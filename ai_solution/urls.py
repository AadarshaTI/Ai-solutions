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
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve as media_serve

urlpatterns = [
    # Built-in Django admin (superuser only)
    path('django-admin/', admin.site.urls),

    # Core application routes (public + staff dashboard)
    path('', include('core.urls')),
]

# Serve uploaded/committed media files.
# WhiteNoise only serves STATIC_ROOT, and the DEBUG-only static() helper is a
# no-op in production — without this route, every ImageField URL (gallery,
# events, testimonials, case-study logos) 404s once DEBUG=False.
urlpatterns += [
    re_path(
        r'^media/(?P<path>.*)$',
        media_serve,
        {'document_root': settings.MEDIA_ROOT},
    ),
]
