release: python manage.py migrate --noinput
web: bash -c "python create_superuser_from_env.py || true; gunicorn inventory_management.wsgi:application --bind 0.0.0.0:\$PORT --workers 2 --timeout 120"

