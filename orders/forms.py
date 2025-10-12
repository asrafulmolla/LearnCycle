# orders/forms.py
from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'payment_method']
        widgets = {
            'shipping_address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'House #, Road, Area, City, Postal Code',
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400'
            }),
            'payment_method': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-emerald-400 focus:border-emerald-400'
            })
        }