
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def privacy_policy(request):
    return render(request, 'pages/privacy_policy.html')

def terms_of_service(request):
    return render(request, 'pages/terms_of_service.html')

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us')
    else:
        form = ContactForm()
    return render(request, 'pages/contact.html', {'form': form})