FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create static directory
RUN mkdir -p static

# Copy and set permission for entrypoint BEFORE switching to non-root user
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create a non-root user
RUN useradd -m -r django && chown -R django /app /entrypoint.sh
USER django

# Expose the port Render expects
EXPOSE $PORT

# Use entrypoint script
ENTRYPOINT ["/entrypoint.sh"]
