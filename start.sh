#!/bin/bash
set -e

# Use PORT environment variable if set, otherwise default to 8000
PORT=${PORT:-8000}

# Run migrations (optional - can be done manually)
# python manage.py migrate --noinput || true

# Start gunicorn
exec gunicorn inventory_management.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

