# support/urls.py
from django.urls import path
from . import views

app_name = 'support'

urlpatterns = [
    path('', views.ticket_list, name='ticket_list'),
    path('create/', views.create_ticket, name='create_ticket'),
    path('chat/<int:ticket_id>/', views.ticket_chat, name='ticket_chat'),
]