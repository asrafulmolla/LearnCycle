from django.urls import path, include
from rest_framework import routers
from .views import BookViewSet, BookRequestViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'book-requests', BookRequestViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
