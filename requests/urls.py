# requests/urls.py
from django.urls import path
from . import views

app_name = 'requests' # ← This is REQUIRED for namespacing

urlpatterns = [
    path('request/', views.request_book, name='request_book'),
    path('history/', views.request_history, name='request_history'),
    path('<int:request_id>/reply/', views.reply_to_request, name='reply_to_request'),
]