#!/bin/sh

echo "Starting SocketIO application on port 5000..."

exec gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 'run:app'