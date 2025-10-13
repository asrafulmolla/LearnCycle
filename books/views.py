# books/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Book, Category, BannerSlide
from donations.models import Donation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from requests.models import BookRequest
from orders.models import Order


@login_required
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, seller=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity', 1)
        image = request.FILES.get('image')
        
        if not all([title, author, category_id, price, condition, description]):
            messages.error(request, "Please fill all required fields.")
            return redirect('books:edit_book', book_id=book_id)
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category.")
            return redirect('books:edit_book', book_id=book_id)
        
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        
        book.title = title
        book.author = author
        book.category = category
        book.price = price
        book.condition = condition
        book.description = description
        book.quantity = quantity
        if image:
            book.image = image
        book.save()
        
        messages.success(request, "Book updated successfully!")
        return redirect('books:seller_books')
    
    categories = Category.objects.all()
    return render(request, 'books/edit.html', {'book': book, 'categories': categories})

@login_required
def sell_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        description = request.POST.get('description')
        quantity = request.POST.get('quantity', 1)
        image = request.FILES.get('image')
        
        if not all([title, author, category_id, price, condition, description]):
            messages.error(request, "Please fill all required fields.")
            return redirect('books:sell_book')
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category.")
            return redirect('books:sell_book')
        
        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
        
        book = Book.objects.create(
            title=title,
            author=author,
            category=category,
            price=price,
            condition=condition,
            description=description,
            seller=request.user,
            quantity=quantity,
            image=image
        )
        
        # Update user profile
        profile = request.user.profile
        profile.is_seller = True
        profile.total_selling_books += 1
        profile.save()
        
        messages.success(request, "Book listed for sale successfully!")
        return redirect('books:seller_books')
    
    categories = Category.objects.all()
    return render(request, 'books/sell.html', {'categories': categories})

@login_required
def seller_books(request):
    books = Book.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'books/seller_books.html', {'books': books})

def book_list(request):
    categories = Category.objects.all()
    banners = BannerSlide.objects.filter(is_active=True).order_by('order')  # ✅ Fetch banners

    # Get regular books
    books = Book.objects.filter(is_available=True)
    
    # Get approved donations
    approved_donations = Donation.objects.filter(status='approved').select_related('category', 'user')
    
    # Combine both querysets
    all_books = list(books) + list(approved_donations)
    
    # Handle search
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
        approved_donations = approved_donations.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
        all_books = list(books) + list(approved_donations)
    
    # Handle category filter
    category_id = request.GET.get('category')
    if category_id and category_id.isdigit():
        books = books.filter(category_id=category_id)
        approved_donations = approved_donations.filter(category_id=category_id)
        all_books = list(books) + list(approved_donations)
    
   # Handle sorting
    sort = request.GET.get('sort')
    if sort:
        if sort == 'price_low':
            all_books = sorted(
                all_books, 
                key=lambda x: x.price if x.price is not None else float('inf')
            )
        elif sort == 'price_high':
            all_books = sorted(
                all_books, 
                key=lambda x: x.price if x.price is not None else float('-inf'),
                reverse=True
            )
        elif sort == 'title':
            all_books = sorted(all_books, key=lambda x: x.title or "")
        elif sort == '-created_at':
            all_books = sorted(all_books, key=lambda x: x.created_at or "", reverse=True)
        elif sort == 'created_at':
            all_books = sorted(all_books, key=lambda x: x.created_at or "")

    
    return render(request, 'books/list.html', {
        'books': all_books,
        'categories': categories,
        'banners': banners,  # ✅ Pass to template
        'selected_category': int(category_id) if category_id and category_id.isdigit() else None,
        'selected_sort': sort,
        'query': query,
    })


def book_detail(request, id):
    # Try to get from Book model first
    try:
        book = Book.objects.get(id=id)
        related_books = Book.objects.filter(
            category=book.category,
            is_available=True
        ).exclude(id=book.id)[:4]
    except Book.DoesNotExist:
        # If not found, try Donation model
        book = get_object_or_404(Donation, id=id, status='approved')
        related_books = Donation.objects.filter(
            category=book.category,
            status='approved'
        ).exclude(id=book.id)[:4]
    
    return render(request, 'books/detail.html', {
        'book': book,
        'related_books': related_books
    })


def about(request):
    return render(request, 'core/about.html') 


@login_required
def seller_dashboard(request):
    # Show all unfulfilled book requests
    pending_requests = BookRequest.objects.filter(is_fulfilled=False)
    return render(request, 'books/seller_dashboard.html', {
        'pending_requests': pending_requests
    })

@login_required
def sell_book_for_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id, is_fulfilled=False)
    
    if request.method == 'POST':
        # Use same logic as sell_book, but pre-fill title/author
        title = request.POST.get('title', book_request.title)
        author = request.POST.get('author', book_request.author)
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        condition = request.POST.get('condition')
        description = request.POST.get('description', book_request.description)
        image = request.FILES.get('image')
        
        if not all([title, author, category_id, price, condition]):
            messages.error(request, "Please fill all required fields.")
            return redirect('books:sell_book_for_request', request_id)
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            messages.error(request, "Invalid category.")
            return redirect('books:sell_book_for_request', request_id)
        
        # Create the book
        book = Book.objects.create(
            title=title,
            author=author,
            category=category,
            price=price,
            condition=condition,
            description=description,
            seller=request.user,
            image=image
        )
        
        # Link book to request
        book_request.matched_book = book
        book_request.is_fulfilled = True  # Optional: mark as fulfilled
        book_request.save()
        
        messages.success(request, f"Book listed! The requester will be notified.")
        return redirect('books:seller_books')
    
    categories = Category.objects.all()
    return render(request, 'books/sell_for_request.html', {
        'book_request': book_request,
        'categories': categories
    })

@login_required
def seller_orders(request):
    # Get all books sold by this user
    seller_books = Book.objects.filter(seller=request.user)
    # Get orders containing those books
    orders = Order.objects.filter(
        items__book__in=seller_books
    ).distinct().order_by('-created_at')
    return render(request, 'orders/seller_orders.html', {'orders': orders})