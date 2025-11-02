#!/bin/bash
set -e

# Use PORT if set by Railway, otherwise default to 8000
PORT=${PORT:-8000}

# Start gunicorn
exec gunicorn inventory_management.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

