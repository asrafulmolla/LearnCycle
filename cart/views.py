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
    total_price = sum(item.book.price * item.quantity for item in cart_items)
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def cart_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, f"Added {book.title} to your cart.")
    return redirect('cart_detail')

@login_required
def cart_remove(request, book_id):
    cart = Cart.objects.get(user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, book__id=book_id)
    cart_item.delete()
    messages.success(request, "Removed item from cart.")
    return redirect('cart_detail')

@login_required
def cart_clear(request):
    cart = Cart.objects.get(user=request.user)
    cart.cartitem_set.all().delete()  # ✅ Use default reverse relation name
    messages.success(request, "Cart cleared.")
    return redirect('cart_detail')