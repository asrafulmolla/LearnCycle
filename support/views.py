# support/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SupportTicket, ChatMessage
from .forms import SupportTicketForm

@login_required
def ticket_list(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'support/ticket_list.html', {'tickets': tickets})

@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Support ticket created!")
            return redirect('support:ticket_list')
    else:
        form = SupportTicketForm()
    return render(request, 'support/create_ticket.html', {'form': form})

@login_required
def ticket_chat(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    messages = ticket.messages.all().order_by('timestamp')
    return render(request, 'support/ticket_chat.html', {
        'ticket': ticket,
        'messages': messages
    })