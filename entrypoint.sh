#!/bin/sh
set -e  # Exit immediately if a command exits with a non-zero status

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput || true

echo "Creating superuser if not exists..."
python manage.py shell << 'END'
from django.contrib.auth import get_user_model
User = get_user_model()
username = "admin"
email = "admin@gmail.com"
password = "admin098"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("✅ Superuser created successfully!")
else:
    print("ℹ️ Superuser already exists.")
END

echo "Starting Gunicorn server..."
exec gunicorn docSys.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --threads 2 \
    --timeout 120
