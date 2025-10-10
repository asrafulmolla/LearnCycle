from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BookRequest
from .forms import BookRequestForm

@login_required
def request_book(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.user = request.user
            book_request.save()
            messages.success(request, "Your book request has been submitted!")
            return redirect('request_history')
    else:
        form = BookRequestForm()
    return render(request, 'requests/request_form.html', {'form': form})

@login_required
def request_history(request):
    requests = BookRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'requests/history.html', {'requests': requests})