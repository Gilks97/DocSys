#!/usr/bin/env bash
set -o errexit

# This script runs inside Render's build environment
echo "Building Django application..."

# Apply migrations (Render will run this during deploy)
python manage.py migrate --no-input

echo "Build completed successfully!"
