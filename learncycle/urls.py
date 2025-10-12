
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('donations/', include('donations.urls')),
    path('orders/', include('orders.urls')),
    path('requests/', include('requests.urls')),
    path('library/', include('library.urls')),
    path('support/', include('support.urls')),
    path('', include('pages.urls')),
    path('', include('books.urls')),   # Root URL directs to books app
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)