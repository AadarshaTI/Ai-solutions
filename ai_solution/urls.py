"""
ai_solution/urls.py
====================
Root URL dispatcher for the AI-Solution project.
Mounts:
  - Django admin  → /admin/
  - Core app      → / (all public & staff-facing routes)
  - Media serving → handled in DEBUG mode only
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Built-in Django admin (superuser only)
    path('django-admin/', admin.site.urls),

    # Core application routes (public + staff dashboard)
    path('', include('core.urls')),
]

# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
