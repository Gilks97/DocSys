# ===============================
# 1 Use an official Python image
# ===============================
FROM python:3.10-slim

# Prevent Python from writing pyc files and buffer issues
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Render automatically sets PORT=10000
ENV PORT=10000

# ===============================
# 2 Set working directory
# ===============================
WORKDIR /app

# ===============================
# 3 Install system dependencies
# ===============================
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# 4 Install Python dependencies
# ===============================
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --timeout=120 --retries=5 -r requirements.txt

# ===============================
# 5 Copy project files
# ===============================
COPY . .

# ===============================
# 6 Collect static files
# ===============================
RUN python manage.py collectstatic --noinput

# ===============================
# 7 Add entrypoint script
# ===============================
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# ===============================
# 8 Create a non-root user
# ===============================
RUN useradd -m -r django && chown -R django /app /entrypoint.sh
USER django

# ===============================
# 9 Expose the Render port
# ===============================
EXPOSE $PORT

# ===============================
# 10 Set the entrypoint
# ===============================
ENTRYPOINT ["/entrypoint.sh"]
