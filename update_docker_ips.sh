#!/bin/bash

MARIADB_RUNNING=$(docker ps --format "{{.Names}}" | grep mariadb)
REDIS_RUNNING=$(docker ps --format "{{.Names}}" | grep redis)

if [[ -z "$MARIADB_RUNNING" || -z "$REDIS_RUNNING" ]]; then
    echo "containers are not running, starting them..."
    docker compose up -d
    echo "waiting for containers to start..."
    sleep 10
fi

# create environment variable file
ENV_FILE=".env"

# get MariaDB IP address
MARIADB_IP=$(docker inspect mariadb --format '{{ .NetworkSettings.Networks.homelette_network.IPAddress }}')
echo "MariaDB IP: $MARIADB_IP"

# get Redis IP address
REDIS_IP=$(docker inspect redis --format '{{ .NetworkSettings.Networks.homelette_network.IPAddress }}')
echo "Redis IP: $REDIS_IP"

# create or update environment variable file
echo "MARIADB_IP=$MARIADB_IP" > $ENV_FILE
echo "REDIS_IP=$REDIS_IP" >> $ENV_FILE

echo "environment variables updated to $ENV_FILE"

# check if flask-socket is running
FLASK_SOCKET_RUNNING=$(docker ps --format "{{.Names}}" | grep flask-socket)

echo "restarting flask-socket container..."
docker compose up -d flask-socket
sleep 5

echo "flask-socket container updated"

echo "operation completed. IP addresses updated and applied to services." 