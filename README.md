
# Social Network API
## Description

A Django-based REST API for social networking application managing friend requests and friendships. Users can search friends,send, accept, and reject friend requests and list their friends.

## Features

- Signup
- Login
- Search Friends by name or email
- Send friend requests
- Accept friend requests
- Reject friend requests
- List friends based on request status

## Installation

### Prerequisites

- Python 3.x
- Django 4.x
- Docker
- Other dependencies as listed in `requirements.txt`

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ramkishor-hosamane/Social-Network-AccuKnox.git
   ```
2. Navigate into the project directory:
   ```bash
   cd social_network
   ```
3. Build the docker image:
   
   Note : while building docker image 100 test users will be created
   
   ```bash
   docker build -t <tagname> .
   ```
4. Run the docker container:
   ```bash
   docker run -p 8000:8000 <tagname>
   ```

## API Endpoints

## Overview

This API provides functionalities for user authentication, searching users, and managing friend requests. Below is the documentation for each endpoint, including the required request data and expected responses.
## Postman Collection
You can import all apis into postman using ```Social Network API.postman_collection.json``` file
## Authentication

Except for the signup and login endpoints, every request must include the `Authorization` header with the user's token:
```
Authorization: Token <user-token>
```

## Endpoints

### 1. User Signup

**Endpoint:** `/api/signup/`

**Method:** `POST`

**Description:** Allows a user to sign up using their email and password.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123",
    "name": "John Doe"
}
```

**Response:**
```json
{
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "full_name": "John Doe"
}
```

### 2. User Login

**Endpoint:** `/api/login/`

**Method:** `POST`

**Description:** Allows a user to log in using their email and password.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "detail": "Login successful",
    "token": "your_auth_token"
}
```

### 3. Search Users

**Endpoint:** `/api/search/`

**Method:** `GET`

**Description:** Allows authenticated users to search for other users by email or name. The search results are paginated with up to 10 records per page.

**Headers:**
```
Authorization: Token <user-token>
```

**Query Parameters:**
- `query`: The search keyword (either email or name).

**Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "email": "user@example.com",
            "name": "John Doe"
        }
    ]
}
```

### 4. Send Friend Request

**Endpoint:** `/api/friend-request/`

**Method:** `POST`

**Description:** Allows an authenticated user to send a friend request to another user. Users can send a maximum of 3 friend requests per minute.

**Headers:**
```
Authorization: Token <user-token>
```

**Request Body:**
```json
{
    "to_user_id": 2
}
```

**Response:**
```json
{
    "id": 1,
    "from_user": "user1@example.com",
    "to_user": "user2@example.com",
    "status": "pending",
    "created_at": "2024-06-07T12:34:56Z"
}
```

**Throttle Error Response:**
```json
{
    "detail": "Request was throttled. Expected available in 42 seconds."
}
```

### 5. List Friend Requests

**Endpoint:** `/api/friend-requests/`

**Method:** `GET`

**Description:** Allows an authenticated user to list all pending friend requests they have received.

**Headers:**
```
Authorization: Token <user-token>
```

**Response:**
```json
[
    {
        "id": 1,
        "from_user": "user1@example.com",
        "to_user": "user2@example.com",
        "status": "pending",
        "created_at": "2024-06-07T12:34:56Z"
    }
]
```

### 6. List Friends

**Endpoint:** `/api/friends/`

**Method:** `GET`

**Description:** Allows an authenticated user to list all their friends (users who have accepted friend requests).

**Headers:**
```
Authorization: Token <user-token>
```

**Response:**
```json
[
    {
        "id": 2,
        "email": "friend@example.com",
        "name": "Friend Name"
    }
]
```

### 7. Update Friend Request

**Endpoint:** `/api/friend-request/<int:pk>/update/`

**Method:** `POST`

**Description:** Allows an authenticated user to accept or reject a pending friend request.

**Headers:**
```
Authorization: Token <user-token>
```

**Request Body:**
```json
{
    "action": "accept"
}
```
or
```json
{
    "action": "reject"
}
```

**Response for Accept:**
```json
{
    "status": "accepted"
}
```

**Response for Reject:**
```json
{
    "status": "rejected"
}
```

## Models

### User

**Fields:**
- `id`: Integer
- `email`: String
- `name`: String
- `password`: String (hashed)
- `full_name`: String (read-only)

### FriendRequest

**Fields:**
- `id`: Integer
- `from_user`: User (ForeignKey)
- `to_user`: User (ForeignKey)
- `status`: String (choices: 'pending', 'accepted', 'rejected')
- `created_at`: DateTime

## Throttling

Users can send a maximum of 3 friend requests per minute. If this limit is exceeded, the following error message is returned:

```json
{
    "detail": "Request was throttled. Expected available in 42 seconds."
}
```

The `42 seconds` part will vary based on how long until the throttle resets.

---
