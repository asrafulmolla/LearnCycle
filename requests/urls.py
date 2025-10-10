from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_book, name='request_book'),
    path('history/', views.request_history, name='request_history'),
]