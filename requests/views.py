# requests/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import BookRequest
from .forms import BookRequestForm
from django.utils import timezone

@login_required
def request_book(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            book_request = form.save(commit=False)
            book_request.user = request.user
            book_request.save()
            messages.success(request, "Your book request has been submitted!")
            return redirect('requests:request_history')
    else:
        form = BookRequestForm()
    return render(request, 'requests/request_form.html', {'form': form})

@login_required
def request_history(request):
    requests = BookRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'requests/history.html', {'requests': requests})

@login_required
def reply_to_request(request, request_id):
    book_request = get_object_or_404(BookRequest, id=request_id)
    if request.method == 'POST':
        reply_message = request.POST.get('reply_message', '')
        book_request.reply_message = reply_message
        book_request.replied_at = timezone.now()
        book_request.save()
        messages.success(request, "Reply sent successfully!")
        return redirect('requests:request_history')
    return render(request, 'requests/reply.html', {'book_request': book_request})