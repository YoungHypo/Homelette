# Homelette Design & Structure

Homelette is a mobile app designed to connect subletters with subtenants in Isla Vista. 
This directory contains all **backend source code** for the project.

## System Architecture

```
           ┌─── backend-api (REST API, port 5001)
           │         ↓ ↑
Client ────┤       MariaDB 
           │         ↑ ↓
           └─── backend-socket (WebSocket, port 5002)
                     ↑ ↓
                    Redis
```

## Service Components

- **flask-api**: Handles REST API requests and data processing
- **flask-socket**: Handles WebSocket connections and real-time chat
- **mariadb**: Database service for persistent storage
- **redis**: Message queue and shared storage for WebSocket communications

## Access Methods

Each service is accessed directly through its dedicated port:

- **REST API**: http://localhost:5001/api/
- **WebSocket**: http://localhost:5002/socket

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

## Continuous Integration

The project uses GitHub Actions for **CI/CD** processes to ensure code reliability:

```bash
# CI checks include:
# - Building all Docker images
# - Starting the services
# - Verifying container health
# - Testing API endpoints
```

- **Location**: `.github/workflows/docker-image.yml`
- **Trigger**: Automatically runs on push to main branch and pull requests
