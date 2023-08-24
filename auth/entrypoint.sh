#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z postgres 5432; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate

exec "$@"