# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DigitalBook

@receiver(post_save, sender=DigitalBook)
def generate_pdf_cover(sender, instance, created, **kwargs):
    if created and not instance.cover_image:
        instance.generate_cover_from_pdf()
