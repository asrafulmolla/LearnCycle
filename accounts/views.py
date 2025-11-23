from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import UserUpdateForm, ProfileUpdateForm
from requests.models import BookRequest

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone = request.POST.get('full_phone')
            address = request.POST.get('address')
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone = phone
            profile.address = address
            profile.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "You’ve been logged out successfully.")
    return redirect('login')

@login_required
def profile(request):
    profile_obj, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile_obj)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile_obj)


    matched_requests = BookRequest.objects.filter(
        user=request.user,
        is_fulfilled=True,
        matched_book__isnull=False
    ).select_related('matched_book')


    donation_requests = BookRequest.objects.filter(
        user=request.user,
        donation__isnull=False
    ).select_related('donation')
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'matched_requests': matched_requests,
        'donation_requests': donation_requests, 
    }
    return render(request, 'accounts/profile.html', context)