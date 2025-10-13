# cart/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from books.models import Book

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    # Add subtotal for each item
    for item in cart_items:
        item.subtotal = item.book.price * item.quantity
    total_price = sum(item.subtotal for item in cart_items)
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def cart_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    # ✅ Prevent user from adding their own book
    if book.seller == request.user:
        messages.error(request, "You cannot add your own book to the cart.")
        return redirect('books:book_detail', id=book.id)
    
    # ✅ Prevent adding if not available
    if not book.is_available:
        messages.error(request, "This book is not available for purchase.")
        return redirect('books:book_detail', id=book.id)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Since no quantity field, assume 1 copy per book
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': 1}
    )
    
    if not created:
        messages.info(request, "This book is already in your cart.")
    else:
        messages.success(request, f'"{book.title}" has been added to your cart.')
    
    return redirect('cart:cart_detail')

@login_required
def cart_remove(request, book_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, book__id=book_id)
    cart_item.delete()
    messages.success(request, "Removed item from cart.")
    return redirect('cart:cart_detail')

@login_required
def cart_clear(request):
    cart = Cart.objects.get(user=request.user)
    cart.cartitem_set.all().delete()  
    messages.success(request, "Cart cleared.")
    return redirect('cart:cart_detail')

@login_required
def cart_update_quantity(request, book_id):
    cart = Cart.objects.get(user=request.user)
    item = get_object_or_404(CartItem, cart=cart, book__id=book_id)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "increase":
            item.quantity += 1
        elif action == "decrease" and item.quantity > 1:
            item.quantity -= 1
        item.save()
    return redirect('cart:cart_detail')