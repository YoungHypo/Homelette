#!/bin/sh

echo "waiting for database..."
sleep 10

echo "executing database migrations..."
flask db upgrade

echo "starting flask application..."
exec gunicorn --bind 0.0.0.0:5000 run:app 