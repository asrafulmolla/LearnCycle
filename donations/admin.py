from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    actions = ['approve_donations']

    def approve_donations(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} donations approved and points awarded!")
    approve_donations.short_description = "Approve selected donations"