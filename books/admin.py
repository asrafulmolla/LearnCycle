from django.contrib import admin
from .models import Book, Category, BannerSlide

admin.site.register(Book)
admin.site.register(Category)

@admin.register(BannerSlide)
class BannerSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_type', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'media_type']
    list_editable = ['order', 'is_active']
    search_fields = ['title', 'description']
    ordering = ['order', '-created_at']