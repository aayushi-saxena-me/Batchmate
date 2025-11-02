"""
WSGI config for inventory_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Auto-detect production environment
# Use production settings if DATABASE_URL exists (Railway/Render/production)
# Otherwise use development settings
if os.environ.get('DATABASE_URL') or os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RENDER'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

application = get_wsgi_application()

