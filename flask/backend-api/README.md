# Homelette Backend API

Homelette is a mobile application platform targeting short-term rental needs of college students, aiming to solve the lack of convenient communication channels between landlords and renters. 
This directory contains the API service of Homelette, responsible for handling all **HTTP** requests.

## Deployment

- **Port**: Service exposed on port 5001
- **Direct Access**: API endpoints are directly accessible without a proxy
- **Authentication**: JWT-based authentication is used for securing endpoints

## API Documentation

### Authentication API

| Function | Method | URL | Parameters |
|------|------|-----|------|
| Register | POST | `/api/auth/register` | email, password, first_name, last_name, major, graduation_year |
| Login | POST | `/api/auth/login` | email, password |

### User Management API

| Function | Method | URL | Parameters |
|------|------|-----|------|
| Get User Profile | GET | `/api/users/{user_id}` | Path parameter: user_id |
| Update User Profile | PUT | `/api/users/{user_id}` | Path parameter: user_id<br>Request body: fields to update |

### Listing Management API

| Function | Method | URL | Parameters |
|------|------|-----|------|
| Get Listings | GET | `/api/listings` | price_min, price_max, bedrooms, city, start_date, end_date |
| Get Listing Details | GET | `/api/listings/{listing_id}` | listing_id |
| Create Listing | POST | `/api/listings` | Request body: address, property, listing information |
| Update Listing | PUT | `/api/listings/{listing_id}` | listing_id<br>Request body: fields to update |
| Delete Listing | DELETE | `/api/listings/{listing_id}` | listing_id |
| Upload Image | POST | `/api/listings/upload-image` | image file |

### Chat API

| Function | Method | URL | Parameters |
|------|------|-----|------|
| Get Conversations | GET | `/api/chat/conversations` | None |
| Create Conversation | POST | `/api/chat/conversations` | participants, title(optional) |
| Get Conversation Details | GET | `/api/chat/conversations/{conversation_id}` | conversation_id |
| Get Conversation Messages | GET | `/api/chat/conversations/{conversation_id}/messages` | conversation_id |
| Get Direct Messages | GET | `/api/chat/messages/direct?user_id={user_id}` | user_id |
| Mark Message as Read | PUT | `/api/chat/messages/{message_id}/read` | message_id |

## Database Management

- Homelette uses MariaDB relational database with SQLAlchemy ORM for data access
- The API service is responsible for all database migrations
- Both API and Socket services share the same database models and schema

## Database Design

### User Table (users)

| Field Name | Type | Description | Constraints |
|------|------|-----|------|
| user_id | VARCHAR(36) | Unique user identifier | Primary Key |
| email | VARCHAR(255) | User email | Unique, Not Null |
| password_hash | VARCHAR(255) | Password hash value | Not Null |
| first_name | VARCHAR(50) | First name | Not Null |
| last_name | VARCHAR(50) | Last name | Not Null |
| major | VARCHAR(100) | Major | Nullable |
| graduation_year | INT | Graduation year | Nullable |
| profile_image | VARCHAR(255) | Profile image URL | Nullable |
| bio | TEXT | Personal biography | Nullable |
| created_at | DATETIME | Creation time | Not Null, Default current time |
| updated_at | DATETIME | Update time | Not Null, Default current time |

### Property Table (properties)

| Field Name | Type | Description | Constraints |
|------|------|-----|------|
| property_id | VARCHAR(36) | Unique property identifier | Primary Key |
| owner_id | VARCHAR(36) | Owner ID | Foreign Key(users.user_id) |
| address_line1 | VARCHAR(255) | Address line 1 | Not Null |
| address_line2 | VARCHAR(255) | Address line 2 | Nullable |
| city | VARCHAR(100) | City | Not Null |
| state | VARCHAR(100) | State/Province | Not Null |
| zip_code | VARCHAR(20) | ZIP code | Not Null |
| property_type | VARCHAR(50) | Property type (apartment/villa etc.) | Not Null |
| bedrooms | INT | Number of bedrooms | Not Null |
| bathrooms | FLOAT | Number of bathrooms | Not Null |
| created_at | DATETIME | Creation time | Not Null, Default current time |
| updated_at | DATETIME | Update time | Not Null, Default current time |

### Listing Table (listings)

| Field Name | Type | Description | Constraints |
|------|------|-----|------|
| listing_id | VARCHAR(36) | Unique listing identifier | Primary Key |
| property_id | VARCHAR(36) | Associated property ID | Foreign Key(properties.property_id) |
| title | VARCHAR(255) | Listing title | Not Null |
| description | TEXT | Listing description | Not Null |
| price | DECIMAL(10,2) | Rent per month | Not Null |
| start_date | DATE | Available move-in date | Not Null |
| end_date | DATE | Lease end date | Not Null |
| is_available | BOOLEAN | Availability status | Not Null, Default TRUE |
| created_at | DATETIME | Creation time | Not Null, Default current time |
| updated_at | DATETIME | Update time | Not Null, Default current time |

### User Interest Table (user_interests)

| Field Name | Type | Description | Constraints |
|------|------|-----|------|
| user_id | VARCHAR(36) | User ID | Foreign Key(users.user_id), Composite Primary Key |
| listing_id | VARCHAR(36) | Listing ID | Foreign Key(listings.listing_id), Composite Primary Key |
| created_at | DATETIME | Creation time | Not Null, Default current time |

### Conversation Table (conversations)

| Field Name | Type | Description | Constraints |
|------|------|-----|------|
| conversation_id | VARCHAR(36) | Unique conversation identifier | Primary Key |
| title | VARCHAR(255) | Conversation title | Nullable |
| created_at | DATETIME | Creation time | Not Null, Default current time |
| updated_at | DATETIME | Update time | Not Null, Default current time |

### Conversation Participant Table (conversation_participants)

| Field Name | Type | Description | Constraints |
|------|------|-----|------|
| conversation_id | VARCHAR(36) | Conversation ID | Foreign Key(conversations.conversation_id), Composite Primary Key |
| user_id | VARCHAR(36) | User ID | Foreign Key(users.user_id), Composite Primary Key |
| joined_at | DATETIME | Join time | Not Null, Default current time |

### Message Table (messages)

| Field Name | Type | Description | Constraints |
|------|------|-----|------|
| message_id | VARCHAR(36) | Unique message identifier | Primary Key |
| sender_id | VARCHAR(36) | Sender ID | Foreign Key(users.user_id), Not Null |
| recipient_id | VARCHAR(36) | Recipient ID (private chat) | Foreign Key(users.user_id), Nullable |
| conversation_id | VARCHAR(36) | Conversation ID (group chat) | Foreign Key(conversations.conversation_id), Nullable |
| content | TEXT | Message content | Not Null |
| is_read | BOOLEAN | Read status | Not Null, Default FALSE |
| timestamp | DATETIME | Send time | Not Null, Default current time |

## Database Relationship Diagram

```
users ────┬─── properties ─── listings
          │         │
          │         └─── user_interests
          │
          ├─── conversation_participants ─── conversations
          │
          └─── messages
```