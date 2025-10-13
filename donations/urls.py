# donations/urls.py
from django.urls import path
from . import views

app_name = 'donations' 

urlpatterns = [
    path('donate/', views.donate_book, name='donate_book'),
    path('history/', views.donation_history, name='donation_history'),
    path('request/<int:id>/', views.request_donated_book, name='request_donated_book'),
    path('confirm-handover/<int:donation_id>/', views.confirm_donation_handover, name='confirm_donation_handover'),
    path('confirm-received/<int:donation_id>/', views.confirm_donation_received, name='confirm_donation_received'),
]