#!/bin/sh

# This script waits for the database to be running
# before starting the server

echo "Waiting for postgreSQL..."

# Wait for database to start
while ! nc -z api-db 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

# run flask server
python manage.py run -h 0.0.0.0

