from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem
from .forms import CheckoutForm
import re

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_detail')

    for item in cart_items:
        item.subtotal = item.book.price * item.quantity

    total_price = sum(item.subtotal for item in cart_items)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        address = request.POST.get('address')
        country_code = request.POST.get('country_code')
        phone = request.POST.get('phone')

        if not all([payment_method, address, phone, country_code]):
            messages.error(request, "Please fill all required fields.")
            return redirect('checkout')

        # Combine country code and number
        full_phone = f"{country_code}{phone}".replace(" ", "")

        # Validate formats (Bangladesh or general)
        pattern_bd = re.compile(r'^\+8801[3-9]\d{8}$')
        pattern_generic = re.compile(r'^\+\d{6,15}$')

        if not (pattern_bd.match(full_phone) or pattern_generic.match(full_phone)):
            messages.error(request, "Please enter a valid phone number (e.g., +8801712345678).")
            return redirect('checkout')

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            status='pending',
            payment_method=payment_method,
            shipping_address=address,
            phone_number=full_phone
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            item.book.is_available = False
            item.book.save()

        cart_items.delete()
        messages.success(request, "Order placed successfully!")
        return redirect('order_success')

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