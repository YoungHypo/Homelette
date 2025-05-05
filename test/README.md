# Homelette Testing Tools

This directory contains test scripts and tools for the backend-socket project.

## Test Scripts

- **socket_dual_test.py**: Tests WebSocket real-time communication functionality
  - Creates two parallel user sessions
  - Tests user registration, login, and authentication
  - Verifies WebSocket connections and message delivery
  - Tests private messaging, typing status, and user online status features

## Installing Dependencies

Test script dependencies can be installed using:

```bash
pip install -r requirements_test.txt
```

## Running Tests

Ensure Homelette services are running (via Docker Compose), then run:

```bash
# Run WebSocket dual-user test
python socket_dual_test.py
```

## Test Environment

- API service should be accessible at `localhost:5001`
- WebSocket service should be accessible at `localhost:5002`
- Tests automatically create temporary user accounts
- All communications use real JWT authentication flows 