from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ]
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='books/', blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['category', 'is_available']),
        ]
    
    def __str__(self):
        return self.title


class BannerSlide(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, blank=True, help_text="Optional title for the slide")
    description = models.TextField(blank=True, help_text="Optional description")
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    image = models.ImageField(upload_to='banners/images/', blank=True, null=True)
    video = models.FileField(upload_to='banners/videos/', blank=True, null=True)
    link_url = models.URLField(blank=True, help_text="Optional URL to link to")
    order = models.IntegerField(default=0, help_text="Order of display (lower numbers first)")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Banner Slide'
        verbose_name_plural = 'Banner Slides'
    
    def __str__(self):
        return self.title or f"Slide {self.id}"
    
    def get_media_url(self):
        if self.media_type == 'image' and self.image:
            return self.image.url
        elif self.media_type == 'video' and self.video:
            return self.video.url
        return None