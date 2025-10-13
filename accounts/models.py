# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

phone_validator = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message="Phone number must be entered in the format: '+8801XXXXXXXXX' (10–15 digits)."
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(region='BD', blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True) 
    book_points = models.IntegerField(default=0)
    image = models.ImageField(upload_to='profile_pics/', default='default_user.png', blank=True)
    
    # New role flags
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_donor = models.BooleanField(default=False)
    total_selling_books = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()