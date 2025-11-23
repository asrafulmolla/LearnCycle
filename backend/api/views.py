from rest_framework import viewsets, permissions
from .models import Book, BookRequest, Category
from .serializers import BookSerializer, BookRequestSerializer, CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookRequestViewSet(viewsets.ModelViewSet):
    queryset = BookRequest.objects.all().order_by('-created_at')
    serializer_class = BookRequestSerializer
    permission_classes = [permissions.AllowAny]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
