from django import forms
from .models import BookRequest

class BookRequestForm(forms.ModelForm):
    class Meta:
        model = BookRequest
        fields = ['title', 'author', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }