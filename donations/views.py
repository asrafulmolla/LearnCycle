# donations/views.py
from django.shortcuts import render, redirect
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