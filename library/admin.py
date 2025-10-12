# admin.py
from django.contrib import admin
from .models import DigitalBook

@admin.register(DigitalBook)
class DigitalBookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'uploaded_by', 'uploaded_at', 'filename')
    readonly_fields = ('uploaded_at',)

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'file', 'cover_image', 'uploaded_by')
        }),
        ('Metadata', {
            'fields': ('uploaded_at',),
        }),
    )

    def has_add_permission(self, request):
        return request.user.is_staff
