# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders' 

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.order_success, name='order_success'),
    path('history/', views.order_history, name='order_history'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/confirm-handover/', views.confirm_handover, name='confirm_handover'),
    path('<int:order_id>/confirm-received/', views.confirm_received, name='confirm_received'),
    path('seller-confirm/<int:order_id>/', views.seller_confirm_order, name='seller_confirm_order'),
    path('seller-cancel/<int:order_id>/', views.seller_cancel_order, name='seller_cancel_order'),
    path('handover-ready/<int:order_id>/', views.mark_handover_ready, name='mark_handover_ready'),
    path('complete/<int:order_id>/', views.complete_order, name='complete_order'),
    path('seller-orders/', views.seller_orders, name='seller_orders'),
]