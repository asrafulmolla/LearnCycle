# donations/forms.py
from django import forms
from .models import Donation
from books.models import Category

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'author', 'category', 'condition', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'condition': forms.Select(choices=[
                ('new', 'New'),
                ('like_new', 'Like New'),
                ('good', 'Good'),
                ('fair', 'Fair'),
            ])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()