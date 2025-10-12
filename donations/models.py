# donations/models.py
from django.db import models
from django.contrib.auth.models import User
from books.models import Category

class Donation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    condition = models.CharField(max_length=20, choices=[
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ])
    description = models.TextField()
    image = models.ImageField(upload_to='donations/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add this property to make it work like a Book
    @property
    def price(self):
        return None  # Donated books are free
    
    @property
    def is_available(self):
        return self.status == 'approved'
    
    @property
    def seller(self):
        return self.user  # For consistency with Book model

    def __str__(self):
        return f"{self.title} by {self.user.username}"