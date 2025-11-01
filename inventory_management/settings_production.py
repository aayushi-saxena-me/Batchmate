"""
Production settings for inventory_management project.
Import base settings and override with production-specific configurations.

To use this, set DJANGO_SETTINGS_MODULE=inventory_management.settings_production
"""
from .settings import *
import os

try:
    import dj_database_url
except ImportError:
    dj_database_url = None
    print("Warning: dj-database-url not installed. Install with: pip install dj-database-url")

# SECURITY SETTINGS - Critical for production
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Generate a new secret key for production or use environment variable
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
if SECRET_KEY == 'django-insecure-change-this-in-production-12345':
    raise ValueError("SECRET_KEY must be set in production environment!")

# Allowed hosts - set your domain here
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',') if os.environ.get('ALLOWED_HOSTS') else []

# Add your domain(s) - remove this comment and add domains:
# ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com', 'your-app.railway.app']

# Database - Use PostgreSQL in production
if dj_database_url and os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback to SQLite if DATABASE_URL not set (for local testing)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Security middleware settings
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static files - Use WhiteNoise for production
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media files - Consider using cloud storage (AWS S3, Cloudinary) for production
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Add WhiteNoise middleware for static files (add to INSTALLED_APPS if using WhiteNoise)
# pip install whitenoise
# Then uncomment:
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Email configuration (for production error reporting)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
    },
}

