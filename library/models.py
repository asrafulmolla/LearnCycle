# models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from pdf2image import convert_from_path
from io import BytesIO
from PIL import Image

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")

class DigitalBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    file = models.FileField(upload_to='ebooks/', validators=[validate_pdf])
    cover_image = models.ImageField(upload_to='ebook_covers/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def filename(self):
        return self.file.name.split('/')[-1]

    def generate_cover_from_pdf(self):
        """Generate first page thumbnail if no cover image uploaded"""
        if not self.cover_image and self.file:
            try:
                pages = convert_from_path(self.file.path, dpi=100, first_page=1, last_page=1)
                if pages:
                    img = pages[0]
                    img_io = BytesIO()
                    img.save(img_io, format='JPEG', quality=85)
                    img_content = ContentFile(img_io.getvalue(), f"{self.pk}_preview.jpg")
                    self.cover_image.save(f"{self.pk}_preview.jpg", img_content, save=False)
                    self.save()
            except Exception as e:
                print("PDF preview generation failed:", e)
