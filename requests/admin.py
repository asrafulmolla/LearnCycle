from django.contrib import admin
from .models import BookRequest

@admin.register(BookRequest)
class BookRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'user', 'is_fulfilled', 'created_at']
    list_filter = ['is_fulfilled', 'created_at']
    actions = ['mark_as_fulfilled']

    def mark_as_fulfilled(self, request, queryset):
        queryset.update(is_fulfilled=True)
        self.message_user(request, f"{queryset.count()} requests marked as fulfilled.")
    mark_as_fulfilled.short_description = "Mark selected requests as fulfilled"