# orders/models.py
from django.db import models
from django.contrib.auth.models import User
from books.models import Book
from donations.models import Donation

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed by Buyer'),
        ('seller_confirmed', 'Confirmed by Seller'),
        ('cancelled', 'Cancelled'),
        ('handover_pending', 'Ready for Handover'),
        ('completed', 'Completed'),
    ]
    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery'),
        ('card', 'Credit/Debit Card'),
        ('mobile', 'Mobile Banking'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cod')
    shipping_address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    country_code = models.CharField(max_length=10, default='+880')
    is_handover_confirmed = models.BooleanField(default=False)
    handover_confirmed_at = models.DateTimeField(null=True, blank=True)
    received_by = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    # Only one of these will be set
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        if self.book:
            return f"{self.quantity} x {self.book.title} (Book)"
        elif self.donation:
            return f"{self.quantity} x {self.donation.title} (Donation)"
        return "Unknown Item"

    @property
    def item(self):
        """Return the actual item (Book or Donation)"""
        return self.book or self.donation

    @property
    def is_donation_item(self):
        return self.donation is not None