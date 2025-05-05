# Homelette WebSocket Server

This directory contains the **WebSocket** service for processing real-time events.

## Technical Stack

- **Flask-SocketIO**: Extension that provides WebSocket support
- **Redis**: Used as a message broker for scaling across multiple instances
- **Gunicorn+Eventlet**: WSGI server optimized for WebSocket connections
- **SQLAlchemy**: ORM for database model access (shared with API service)

## WebSocket Event API

### Connection Events

| Event | Payload | Description |
|-------|---------|-------------|
| `connect` | `{ token: "JWT_TOKEN" }` (via URL query parameter) | Establishes WebSocket connection using JWT authentication |
| `disconnect` | None | Terminates WebSocket connection |

### User Status Events

| Event | Payload | Description |
|-------|---------|-------------|
| `user_online` | `{ user_id: "uuid" }` | Notifies clients when a user comes online |
| `user_offline` | `{ user_id: "uuid" }` | Notifies clients when a user goes offline |
| `online_users` | `{ users: ["user_id1", "user_id2", ...] }` | Sends the complete list of currently online users |

### Chat Room Events

| Event | Payload | Description |
|-------|---------|-------------|
| `join_conversation` | `{ conversation_id: "uuid" }` | User joins a specific conversation room |
| `leave_conversation` | `{ conversation_id: "uuid" }` | User leaves a specific conversation room |

### Messaging Events

| Event | Payload | Description |
|-------|---------|-------------|
| `private_message` | `{ sender_id: "uuid", recipient_id: "uuid", content: "message" }` | Sends a direct message to a specific user |
| `conversation_message` | `{ sender_id: "uuid", conversation_id: "uuid", content: "message" }` | Sends a message to all users in a conversation |
| `message_delivered` | Message object with all metadata | Confirms message delivery and provides complete message details |

### UI Interaction Events

| Event | Payload | Description |
|-------|---------|-------------|
| `typing` | `{ user_id: "uuid", recipient_id: "uuid" OR conversation_id: "uuid", is_typing: boolean }` | Indicates user is typing (or stopped typing) |
| `user_typing` | `{ user_id: "uuid", is_typing: boolean }` | Notifies that a user is typing in the conversation |

## Notes

- This service is directly exposed on port 5002
- JWT token is passed as a URL query parameter: `http://localhost:5002?token=<JWT_TOKEN>`
- Database models are shared with the API service, but **migrations** should be performed via the API service