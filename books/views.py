# books/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Book, Category, BannerSlide
from donations.models import Donation

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