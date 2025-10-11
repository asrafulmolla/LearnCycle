from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')
    
    if request.method == 'POST':
        # Create order
        total = sum(item.book.price * item.quantity for item in cart_items)
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status='pending'
        )
        
        # Create order items and mark books as unavailable
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            item.book.is_available = False
            item.book.save()
        
        # Clear cart
        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('order_success')
    
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def order_success(request):
    return render(request, 'orders/success.html')

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})