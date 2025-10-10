from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_pdf(value):
    if not value.name.endswith('.pdf'):
        raise ValidationError("Only PDF files are allowed.")

class DigitalBook(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    file = models.FileField(upload_to='ebooks/', validators=[validate_pdf])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def filename(self):
        return self.file.name.split('/')[-1]
