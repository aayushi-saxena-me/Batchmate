#!/bin/bash
set -e

# Start gunicorn on port 8000
exec gunicorn inventory_management.wsgi:application \
    --bind "0.0.0.0:8000" \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -

