# donations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('donate/', views.donate_book, name='donate_book'),
    path('history/', views.donation_history, name='donation_history'),
]