# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.models import Cart, CartItem
from .models import Order, OrderItem
import re
from django.utils import timezone
from books.models import Book
from django.db.models import Case, When, IntegerField

@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_detail')
    
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
            return redirect('orders:checkout')

        full_phone = f"{country_code}{phone}".replace(" ", "")
        pattern_bd = re.compile(r'^\+8801[3-9]\d{8}$')
        pattern_generic = re.compile(r'^\+\d{6,15}$')
        if not (pattern_bd.match(full_phone) or pattern_generic.match(full_phone)):
            messages.error(request, "Please enter a valid phone number (e.g., +8801712345678).")
            return redirect('orders:checkout')

        # Create the order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            status='confirmed',
            payment_method=payment_method,
            shipping_address=address,
            phone_number=full_phone
        )

        # Add items to order and reduce book availability
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price
            )
            # Mark book as unavailable if quantity was 1 (simple logic)
            # Note: If you later add `quantity` field to Book, update this logic
            item.book.is_available = False
            item.book.save()

        # ✅ Mark user as buyer on first purchase
        profile = request.user.profile
        if not profile.is_buyer:
            profile.is_buyer = True
            profile.save()

        # Clear cart
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('orders:order_success')

    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def confirm_handover(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status not in ['delivered', 'handover_pending']:
        messages.error(request, "This order is not ready for handover confirmation.")
        return redirect('orders:order_detail', order_id=order_id)
    
    order.status = 'handover_confirmed'
    order.is_handover_confirmed = True
    order.handover_confirmed_at = timezone.now()
    order.save()
    
    messages.success(request, "Handover confirmed successfully!")
    return redirect('orders:order_detail', order_id=order_id)

@login_required
def confirm_received(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'handover_confirmed':
        messages.error(request, "Handover must be confirmed first.")
        return redirect('orders:order_detail', order_id=order_id)
    
    order.status = 'received'
    order.received_by = request.user.get_full_name() or request.user.username
    order.save()
    
    # Award points if any item is a donation
    for item in order.items.all():
        if item.donation:
            donor = item.donation.user
            donor.profile.book_points += 10
            donor.profile.save()
            # Finalize donation status
            item.donation.status = 'received'
            item.donation.save()
    
    messages.success(request, "Book received! Points awarded to donor.")
    return redirect('orders:order_detail', order_id=order_id)

@login_required
def order_success(request):
    return render(request, 'orders/success.html')

@login_required
def order_history(request):
    # Define custom sort order: pending/processing first, then delivered, then cancelled
    status_order = Case(
        When(status='pending', then=1),
        When(status='processing', then=2),
        When(status='shipped', then=3),
        When(status='delivered', then=4),
        When(status='cancelled', then=5),
        default=6,
        output_field=IntegerField()
    )
    orders = Order.objects.filter(user=request.user).annotate(
        custom_order=status_order
    ).order_by('custom_order', '-created_at')
    
    return render(request, 'orders/history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/detail.html', {'order': order})

@login_required
def seller_confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # Verify current user is the seller of any item in this order
    if not order.items.filter(book__seller=request.user).exists():
        messages.error(request, "You are not the seller of this order.")
        return redirect('profile')
    
    order.status = 'seller_confirmed'
    order.save()
    messages.success(request, "Order confirmed!")
    return redirect('orders:seller_orders')

@login_required
def seller_cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.items.filter(book__seller=request.user).exists():
        messages.error(request, "You cannot cancel this order.")
        return redirect('profile')
    
    order.status = 'cancelled'
    order.save()
    # Re-list books as available
    for item in order.items.all():
        item.book.is_available = True
        item.book.save()
    messages.success(request, "Order cancelled and books relisted.")
    return redirect('orders:seller_orders')

@login_required
def mark_handover_ready(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.items.filter(book__seller=request.user).exists():
        messages.error(request, "Access denied.")
        return redirect('profile')
    
    order.status = 'handover_pending'
    order.save()
    messages.success(request, "Order marked ready for handover.")
    return redirect('orders:seller_orders')

@login_required
def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not order.items.filter(book__seller=request.user).exists():
        messages.error(request, "Access denied.")
        return redirect('profile')
    
    order.status = 'completed'
    order.save()
    messages.success(request, "Order completed successfully!")
    return redirect('orders:seller_orders')

@login_required
def seller_orders(request):
    seller_books = Book.objects.filter(seller=request.user)
    orders = Order.objects.filter(items__book__in=seller_books).distinct().order_by('-created_at')
    return render(request, 'orders/seller_orders.html', {'orders': orders})