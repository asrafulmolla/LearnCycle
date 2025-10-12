from django import forms
from .models import ContactMessage

# pages/forms.py
class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-emerald-400'}),
            'email': forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-emerald-400'}),
            'subject': forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-emerald-400'}),
            'message': forms.Textarea(attrs={'class': 'w-full border border-gray-300 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-emerald-400', 'rows': 4}),
        }

