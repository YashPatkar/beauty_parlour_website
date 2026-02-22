"""
Main URL configuration. All routes point to app urls.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_panel/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('', include('services.urls')),
    path('bookings/', include('bookings.urls')),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom 404 handler - must be in root urlconf
handler404 = 'services.views.page_not_found'
