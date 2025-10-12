# donations/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donation
from .forms import DonationForm

@login_required
def donate_book(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            messages.success(request, "Thank you for your donation! It's now pending approval.")
            return redirect('donation_history')
    else:
        form = DonationForm()
    return render(request, 'donations/donate.html', {'form': form})

@login_required
def donation_history(request):
    donations = Donation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'donations/history.html', {'donations': donations})


@login_required
def request_donated_book(request, id):
    donation = get_object_or_404(Donation, id=id, status='approved')
    
    # You can create a DonationRequest model later, for now just show a message
    messages.success(request, f'Your request for "{donation.title}" has been submitted. We will contact you soon!')
    
    return redirect('book_list')