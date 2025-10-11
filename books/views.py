from django.shortcuts import render, get_object_or_404
from .models import Book, Category
from django.db.models import Q

def book_list(request):
    # Get all categories for the filter dropdown
    categories = Category.objects.all()
    
    # Start with all available books
    books = Book.objects.filter(is_available=True)

     # === SEARCH ===
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Handle category filter
    category_id = request.GET.get('category')
    if category_id and category_id.isdigit():
        try:
            Category.objects.get(id=category_id)
            books = books.filter(category_id=category_id)
        except Category.DoesNotExist:
            pass  # Ignore invalid category
    
    # Handle sorting
    sort = request.GET.get('sort')
    if sort:
        if sort == 'price_low':
            books = books.order_by('price')
        elif sort == 'price_high':
            books = books.order_by('-price')
        elif sort == 'title':
            books = books.order_by('title')
        elif sort == '-created_at':
            books = books.order_by('-created_at')
        elif sort == 'created_at':
            books = books.order_by('created_at')
        # 'featured' or default: no sorting (or add custom logic)
    
    return render(request, 'books/list.html', {
        'books': books,
        'categories': categories,
        'selected_category': int(category_id) if category_id and category_id.isdigit() else None,
        'selected_sort': sort,
        'query': query,
    })

def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    
    # Get related books from the same category (excluding current book)
    related_books = Book.objects.filter(
        category=book.category,
        is_available=True
    ).exclude(id=book.id)[:4]  # Limit to 4 books
    
    return render(request, 'books/detail.html', {
        'book': book,
        'related_books': related_books
    })