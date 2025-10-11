# support/admin.py
from django.contrib import admin
from .models import SupportTicket, ChatMessage

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    actions = ['close_tickets']

    def close_tickets(self, request, queryset):
        queryset.update(status='closed')
        self.message_user(request, f"{queryset.count()} tickets closed.")
    close_tickets.short_description = "Close selected tickets"

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'sender', 'message', 'timestamp']
    list_filter = ['timestamp']