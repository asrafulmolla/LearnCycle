# cart/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:book_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:book_id>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('update/<int:book_id>/', views.cart_update_quantity, name='cart_update_quantity'),
]