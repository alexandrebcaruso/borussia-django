#!/bin/bash

# Wait for the database to be ready
echo "Waiting for the database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database is ready."

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collecting static files
python manage.py collectstatic --noinput

# Start the server
echo "Starting the server..."
exec gunicorn --bind 0.0.0.0:8000 borussia.wsgi:application