# API Documentation

## User Registration and Authentication API
**Version:** 1.0.0
**Base URL:** http://localhost:5000/api
**Authentication:** JWT (JSON Web Tokens)

---

## Overview
This is a RESTful API for user registration and authentication. The API provides endpoints for user management, authentication, and profile operations with comprehensive error handling and security features.

---

## Authentication
All protected endpoints require a JWT bearer token in the Authorization header.

```
Authorization: Bearer <your_jwt_token>
```

---

## Endpoints

### 1. Health Check
**Endpoint:** `GET /health`
**Authentication:** Not required
**Description:** Check if the API is running and healthy

**Request:**
```http
GET /api/health HTTP/1.1
Host: localhost:5000
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2026-04-15T10:30:00.000000"
}
```

---

### 2. User Registration
**Endpoint:** `POST /auth/register`
**Authentication:** Not required
**Description:** Register a new user account

**Request:**
```http
POST /api/auth/register HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Request Body Parameters:**
| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| username | string | Yes | 3-20 chars, alphanumeric + underscore |
| email | string | Yes | Valid email format |
| password | string | Yes | Min 8 chars, uppercase, lowercase, digit |
| first_name | string | Yes | Min 2 chars, letters/spaces/hyphens |
| last_name | string | Yes | Min 2 chars, letters/spaces/hyphens |

**Response (201 Created):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-04-15T10:30:00.000000",
    "updated_at": "2026-04-15T10:30:00.000000"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Missing or invalid fields
- `409 Conflict` - Username or email already exists

---

### 3. User Login
**Endpoint:** `POST /auth/login`
**Authentication:** Not required
**Description:** Authenticate user and receive JWT token

**Request:**
```http
POST /api/auth/login HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "username": "johndoe",
  "password": "SecurePass123"
}
```

**Request Body Parameters:**
| Field | Type | Required |
|-------|------|----------|
| username | string | Yes |
| password | string | Yes |

**Response (200 OK):**
```json
{
  "message": "Login successful",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-04-15T10:30:00.000000",
    "updated_at": "2026-04-15T10:30:00.000000"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Missing username or password
- `401 Unauthorized` - Invalid credentials

---

### 4. Get User by ID
**Endpoint:** `GET /users/{user_id}`
**Authentication:** Required
**Description:** Retrieve user details by ID

**Request:**
```http
GET /api/users/1 HTTP/1.1
Host: localhost:5000
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "created_at": "2026-04-15T10:30:00.000000",
  "updated_at": "2026-04-15T10:30:00.000000"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing JWT token
- `404 Not Found` - User not found

---

### 5. List All Users
**Endpoint:** `GET /users`
**Authentication:** Required
**Description:** Retrieve list of all registered users

**Request:**
```http
GET /api/users HTTP/1.1
Host: localhost:5000
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-04-15T10:30:00.000000",
    "updated_at": "2026-04-15T10:30:00.000000"
  },
  {
    "id": 2,
    "username": "janedoe",
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-04-15T10:35:00.000000",
    "updated_at": "2026-04-15T10:35:00.000000"
  }
]
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing JWT token

---

### 6. Update User
**Endpoint:** `PUT /users/{user_id}`
**Authentication:** Required
**Description:** Update user profile information

**Request:**
```http
PUT /api/users/1 HTTP/1.1
Host: localhost:5000
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
  "first_name": "Jonathan",
  "email": "jonathan@example.com"
}
```

**Request Body Parameters (all optional):**
| Field | Type | Constraints |
|-------|------|-------------|
| first_name | string | Min 2 chars, letters/spaces/hyphens |
| last_name | string | Min 2 chars, letters/spaces/hyphens |
| email | string | Valid email format |

**Response (200 OK):**
```json
{
  "message": "User updated successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "jonathan@example.com",
    "first_name": "Jonathan",
    "last_name": "Doe",
    "is_active": true,
    "created_at": "2026-04-15T10:30:00.000000",
    "updated_at": "2026-04-15T10:45:00.000000"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Invalid field values
- `401 Unauthorized` - Invalid or missing JWT token
- `404 Not Found` - User not found
- `409 Conflict` - Email already in use

---

### 7. Delete User
**Endpoint:** `DELETE /users/{user_id}`
**Authentication:** Required
**Description:** Delete user account

**Request:**
```http
DELETE /api/users/1 HTTP/1.1
Host: localhost:5000
Authorization: Bearer <jwt_token>
```

**Response (200 OK):**
```json
{
  "message": "User deleted successfully"
}
```

**Error Responses:**
- `401 Unauthorized` - Invalid or missing JWT token
- `404 Not Found` - User not found

---

## Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid input or missing required fields |
| 401 | Unauthorized - Missing or invalid authentication token |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists (duplicate email/username) |
| 500 | Internal Server Error - Unexpected server error |

---

## Error Response Format

All error responses follow this format:

```json
{
  "error": "Descriptive error message"
}
```

---

## Security Considerations

1. **Password Storage:** Passwords are hashed using bcrypt with 12 salt rounds
2. **Authentication:** JWT tokens with 1-hour expiration
3. **Input Validation:** All inputs validated before processing
4. **SQL Prevention:** SQLAlchemy ORM prevents SQL injection
5. **CORS:** Enabled for development, should be restricted in production

---

## Testing the API

### Using curl:
```bash
# Register
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "Test1234",
    "first_name": "Test",
    "last_name": "User"
  }'

# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "Test1234"
  }'

# Get user (replace TOKEN with JWT from login)
curl -X GET http://localhost:5000/api/users/1 \
  -H "Authorization: Bearer TOKEN"
```

### Using Postman:
Import the provided Postman collection for easy testing of all endpoints.

---

## Rate Limiting
Currently not implemented but recommended for production deployment.

---

## Versioning
Current API version is 1.0.0. Version is included in the base URL path for future compatibility.

