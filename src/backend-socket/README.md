# Homelette WebSocket Server

Homelette WebSocket Server is the real-time communication component of the Homelette platform, specifically designed to handle instant messaging and live status updates. 
This service focuses on maintaining **WebSocket** connections and processing real-time events.

## Technical Stack

- **Flask**: Lightweight web framework serving as the foundation
- **Flask-SocketIO**: Extension that provides WebSocket support
- **Redis**: Used as a message broker for scaling across multiple instances
- **Eventlet**: WSGI server optimized for WebSocket connections
- **SQLAlchemy**: ORM for database model access (shared with API service)

## WebSocket Event API

### Connection Events

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `connect` | Client → Server | `{ token: "JWT_TOKEN" }` | Establishes WebSocket connection using JWT authentication |
| `disconnect` | Client → Server | None | Terminates WebSocket connection |

### User Status Events

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `user_online` | Server → Client | `{ user_id: "uuid" }` | Notifies clients when a user comes online |
| `user_offline` | Server → Client | `{ user_id: "uuid" }` | Notifies clients when a user goes offline |
| `online_users` | Server → Client | `{ users: ["user_id1", "user_id2", ...] }` | Sends the complete list of currently online users |

### Chat Room Events

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `join_conversation` | Client → Server | `{ conversation_id: "uuid" }` | User joins a specific conversation room |
| `leave_conversation` | Client → Server | `{ conversation_id: "uuid" }` | User leaves a specific conversation room |

### Messaging Events

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `private_message` | Client → Server | `{ sender_id: "uuid", recipient_id: "uuid", content: "message" }` | Sends a direct message to a specific user |
| `conversation_message` | Client → Server | `{ sender_id: "uuid", conversation_id: "uuid", content: "message" }` | Sends a message to all users in a conversation |
| `message_delivered` | Server → Client | Message object with all metadata | Confirms message delivery and provides complete message details |

### UI Interaction Events

| Event | Direction | Payload | Description |
|-------|-----------|---------|-------------|
| `typing` | Client → Server | `{ user_id: "uuid", recipient_id: "uuid" OR conversation_id: "uuid", is_typing: boolean }` | Indicates user is typing (or stopped typing) |
| `user_typing` | Server → Client | `{ user_id: "uuid", is_typing: boolean }` | Notifies that a user is typing in the conversation |

## Notes

- This service is designed to work behind an Nginx proxy
- Multiple instances can be deployed with Redis as the message queue
- No direct API endpoints are exposed - all communication is through WebSocket events
- Database models are shared with the API service, but migrations should be performed via the API service