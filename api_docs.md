# News Portal API Documentation

This document describes the available REST API endpoints for the News Portal project.  
Authentication is required for most endpoints. Responses are in JSON format.

## Authentication

- Uses Django session authentication or token authentication (if enabled).
- Include your session cookie or token in requests.

## Subscribed Articles

- **Endpoint**: `/api/subscribed-articles/`
- **Method**: GET
- **Auth Required**: Yes (Reader must be logged in)
- **Description**: Returns a list of approved articles from publishers/journalists the reader follows.

### Example Request
```http
GET /api/subscribed-articles/ HTTP/1.1
Host: localhost:8000
Cookie: sessionid=abc123

### Example response
[
  {
    "id": 1,
    "title": "Breaking News",
    "publisher": "Daily Times",
    "author": "Jane Doe",
    "published_at": "2025-11-27T09:00:00Z"
  },
  {
    "id": 2,
    "title": "Weekly Digest",
    "publisher": "Global News",
    "author": "John Smith",
    "published_at": "2025-11-27T10:30:00Z"
  }
]


---

### 5. **Newsletters Endpoint**
```markdown
## Newsletters

- **Endpoint**: `/api/newsletters/`
- **Methods**: GET, POST, PUT, DELETE
- **Auth Required**: Yes (Journalist role)

### Example Request (POST)
```http
POST /api/newsletters/ HTTP/1.1
Host: localhost:8000
Content-Type: application/json
Cookie: sessionid=abc123

{
  "title": "Weekly Digest",
  "content": "Summary of top stories",
  "author": 2
}

### Example Response
{
  "id": 5,
  "title": "Weekly Digest",
  "content": "Summary of top stories",
  "author": 2,
  "created_at": "2025-11-27T11:00:00Z"
}


---

### 6. **Publishers Endpoint**
```markdown
## Publishers

- **Endpoint**: `/api/publishers/`
- **Methods**: GET, POST
- **Auth Required**: Yes (Publisher role)

### Example Response (GET)
```json
[
  {
    "id": 1,
    "name": "Daily Times",
    "created_at": "2025-11-27T08:00:00Z"
  }
]


---

### 7. **Twitter/X Integration**
```markdown
## Twitter/X Integration

- Controlled by `TWITTER_ENABLED` in `.env`.
- When enabled, approving an article posts a tweet:

