"""Django application configuration for AI Solutions."""
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name  = 'core'
    label = 'core'
    verbose_name = 'AI Solutions'
