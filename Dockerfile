
FROM python:3.10-slim

# Prevent Python from buffering output and writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Create static directory
RUN mkdir -p static

# Create a non-root user
RUN useradd -m -r django && chown -R django /app
USER django

# Copy and prepare entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose the port Render expects
EXPOSE $PORT

# Use the entrypoint script to handle migrations, superuser, and start Gunicorn
ENTRYPOINT ["/entrypoint.sh"]
