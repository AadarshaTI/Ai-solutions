#!/usr/bin/env python
"""
manage.py
==========
Django's command-line utility for administrative tasks.
Usage: python manage.py <command>
"""
import os
import sys
from pathlib import Path


def load_local_env():
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    base_dir = Path(__file__).resolve().parent
    load_dotenv(base_dir / ".env.local")
    load_dotenv(base_dir / ".env")


def main():
    load_local_env()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ai_solution.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Ensure it is installed and your "
            "virtual environment is activated."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
