# Homelette Source Code Structure

This directory contains all backend source code for the Homelette project.

## System Architecture

```
                 ┌─── backend-api (REST API Service)
                 │      ↓ ↑
Client → Nginx Proxy ┤      MariaDB
                 │      ↑ ↓
                 └─── backend-socket (WebSocket Service)
                        ↑ ↓
                        Redis
```

## Service Components

- **Nginx**: Reverse proxy server that routes different types of requests to corresponding backend services
- **flask-api**: Handles REST API requests and data processing
- **flask-socket**: Handles WebSocket connections and real-time chat functionality
- **mariadb**: Database service for persistent storage
- **redis**: Message queue and shared storage for WebSocket communications

## Access Methods

All API requests and WebSocket connections are accessed through the Nginx proxy:

- **REST API**: http://localhost/api/...
- **WebSocket**: http://localhost/socket.io/...

## Directory Structure

- **backend-api/**: Contains REST API related code
  - Handles all HTTP requests
  - Implements RESTful API endpoints
  - Contains all data model definitions

- **backend-socket/**: Contains WebSocket related code
  - Manages real-time WebSocket connections
  - Implements chat functionality
  - Manages real-time message broadcasting

- **nginx/**: Contains Nginx reverse proxy configuration
  - Routes requests to appropriate services
  - Configures WebSocket proxy settings

## Development Guide

All services are managed by `docker-compose.yml` in root and can be operated by `make`.

### Run Docker 

```bash
# Build all services
make build

# Start all services
make start
```

### Database Migrations

```bash
# Create and apply migrations in one step
make migrate message="Describe your changes"

# Or execute step by step
make migrate-create message="Describe your changes"
make migrate-apply
```


