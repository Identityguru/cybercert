"""
WSGI entry point — used by Gunicorn in production.

    gunicorn wsgi:app
"""
from src import create_app

app = create_app()
