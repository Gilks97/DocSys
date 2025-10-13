#!/bin/sh

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', 'admin098')
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
END

echo "Starting Gunicorn..."
exec gunicorn docSys.wsgi:application --bind 0.0.0.0:$PORT --workers 3
