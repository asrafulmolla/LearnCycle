from django.shortcuts import render
from .models import Book, Category

def book_list(request):
    books = Book.objects.filter(is_available=True)
    categories = Category.objects.all()
    return render(request, 'books/list.html', {'books': books, 'categories': categories})

def book_detail(request, id):
    book = Book.objects.get(id=id)
    return render(request, 'books/detail.html', {'book': book})