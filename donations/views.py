# donations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donation
from .forms import DonationForm
from orders.models import Order, OrderItem
from django.utils import timezone
from requests.models import BookRequest

@login_required
def donate_book(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            # Mark user as donor
            profile = request.user.profile
            profile.is_donor = True
            profile.save()
            messages.success(request, "Thank you for your donation! It's now pending approval.")
            return redirect('donations:donation_history')
    else:
        form = DonationForm()
    return render(request, 'donations/donate.html', {'form': form})

@login_required
def request_donated_book(request, id):
    donation = get_object_or_404(Donation, id=id, status='approved')
        # Prevent users from requesting their own donations
    if donation.user == request.user:
        messages.error(request, "You cannot request your own donation.")
        return redirect('books:book_list')
    
    BookRequest.objects.create(
        user=request.user,
        title=donation.title,
        author=donation.author,
        description=donation.description,
        donation=donation,
        is_fulfilled=False
    )

    # Create order for donation (as before)
    order = Order.objects.create(
        user=request.user,
        total_price=0,
        status='handover_pending',
        payment_method='cod',
        shipping_address=request.user.profile.address or "",
        phone_number=str(request.user.profile.phone) if request.user.profile.phone else ""
    )
    OrderItem.objects.create(order=order, donation=donation, quantity=1, price=0)
    donation.status = 'requested'
    donation.save()

    # ✅ Also mark as buyer (since they're receiving a book)
    profile = request.user.profile
    if not profile.is_buyer:
        profile.is_buyer = True
        profile.save()

    messages.success(request, f'Your request for "{donation.title}" has been submitted.')
    return redirect('books:book_list')

@login_required
def confirm_donation_handover(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id, user=request.user)
    if donation.status != 'requested':
        messages.error(request, "This donation is not in requested state.")
        return redirect('donations:donation_history')
    
    # Mark as handover confirmed
    donation.status = 'handover_confirmed'
    donation.save()
    
    messages.success(request, "Handover confirmed successfully!")
    return redirect('donations:donation_history')

@login_required
def confirm_donation_received(request, donation_id):
    donation = get_object_or_404(Donation, id=donation_id)
    if donation.status != 'handover_confirmed':
        messages.error(request, "This donation has not been confirmed for handover yet.")
        return redirect('donations:donation_history')
    
    # Award points ONLY here
    donation.status = 'received'
    donation.user.profile.book_points += 10
    donation.user.profile.save()
    donation.save()

@login_required
def donation_history(request):
    donations = Donation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'donations/history.html', {'donations': donations})