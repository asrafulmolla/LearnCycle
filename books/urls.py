# books/urls.py
from django.urls import path
from . import views

app_name = 'books' # ← This is REQUIRED for namespacing

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:id>/', views.book_detail, name='book_detail'),
    path('about/', views.about, name='about'),
    path('sell/', views.sell_book, name='sell_book'),
    path('seller-books/', views.seller_books, name='seller_books'),
    path('edit/<int:book_id>/', views.edit_book, name='edit_book'),
    path('seller-dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('sell-for-request/<int:request_id>/', views.sell_book_for_request, name='sell_book_for_request'),
    path('seller-orders/', views.seller_orders, name='seller_orders'),
]