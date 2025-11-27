#!/usr/bin/env bash
set -e

# Default env fallbacks
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-news_portal.settings}"
export DB_HOST="${DB_HOST:-db}"
export DB_PORT="${DB_PORT:-3306}"

# Wait for DB (explicit bash call for safety)
bash /app/docker/wait-for-db.sh

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --noinput

# Collect static
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Optional: load sample data if desired
if [ "${LOAD_FIXTURES:-0}" = "1" ]; then
  echo "Loading sample data..."
  python manage.py loaddata sample_data.json || echo "No fixtures loaded."
fi

# Start server
echo "Starting Django..."
exec python manage.py runserver 0.0.0.0:8000
