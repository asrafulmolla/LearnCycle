# donations/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('donate/', views.donate_book, name='donate_book'),
    path('history/', views.donation_history, name='donation_history'),
    path('request/<int:id>/', views.request_donated_book, name='request_donated_book'),
]