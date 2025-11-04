release: python manage.py migrate --noinput && (python create_superuser_from_env.py || echo "Superuser creation skipped - OK if not configured")
web: gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120

