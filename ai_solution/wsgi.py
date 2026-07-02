"""
ai_solution/wsgi.py
====================
WSGI entry-point for production deployment.
"""
import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv:
    BASE_DIR = Path(__file__).resolve().parent.parent
    load_dotenv(BASE_DIR / ".env.local")
    load_dotenv(BASE_DIR / ".env")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_solution.settings')
application = get_wsgi_application()
