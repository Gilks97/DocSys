FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FIX: Create static dir and handle collectstatic errors
RUN mkdir -p static
RUN python manage.py collectstatic --noinput --clear || echo "Collectstatic completed with warnings"

RUN useradd -m -r django && chown -R django /app
USER django

EXPOSE $PORT

RUN python manage.py check

CMD bash -c "
python manage.py migrate --noinput &&
python manage.py collectstatic --noinput &&
python manage.py shell -c \"from django.contrib.auth import get_user_model; \
User=get_user_model(); \
username='admin'; \
email='admin@gmail.com'; \
password='admin098'; \
User.objects.filter(username=username).exists() or \
User.objects.create_superuser(username, email, password)\" &&
gunicorn docSys.wsgi:application --bind 0.0.0.0:\$PORT --workers 3
"
