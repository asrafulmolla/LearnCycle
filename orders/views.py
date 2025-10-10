from django.shortcuts import render, redirect
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Order, OrderItem

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')
    
    # Create order
    order = Order.objects.create(user=request.user, is_paid=True)
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )
        # Optional: mark book as unavailable
        item.book.is_available = False
        item.book.save()
    
    # Clear cart
    cart_items.delete()
    messages.success(request, "Order placed successfully!")
    return redirect('order_success')

def order_success(request):
    return render(request, 'orders/success.html')