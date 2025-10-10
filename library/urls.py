from django.urls import path
from . import views

urlpatterns = [
    path('', views.library_list, name='library_list'),
    path('download/<int:pk>/', views.library_download, name='library_download'),
]