release: python manage.py migrate --noinput && echo "Migrations completed successfully"
web: bash -c "sleep 2 && python create_superuser_from_env.py || true; gunicorn inventory_management.wsgi:application --bind 0.0.0.0:\$PORT --workers 2 --timeout 120"

