# Construction Project Management API Documentation

## Overview

This document describes the REST API contract for the Construction Project Management system. The API provides CRUD operations for Projects and Locations with comprehensive filtering, validation, and error handling.

## Base URL

```
http://localhost:8000
```

## Authentication

Not implemented in v1.0.0 (single-user MVP). Future versions will support JWT/OAuth2.

## Content Type

All requests and responses use `application/json`.

## HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success (GET, PUT) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 404 | Resource Not Found |
| 422 | Validation Error |
| 500 | Internal Server Error |

## Data Models

### ProjectStatus Enum
- `active` - Project is currently ongoing
- `completed` - Project has been finished
- `on-hold` - Project is temporarily paused

### Coordinates Object
```json
{
  "lat": 40.7128,    // Latitude: -90 to 90
  "lng": -74.0060    // Longitude: -180 to 180
}
```

## Endpoints

### Projects

#### 1. List Projects
```
GET /api/projects
```

**Query Parameters:**
- `status` (optional): Filter by status (active|completed|on-hold)
- `start_date_from` (optional): Filter projects starting from date (YYYY-MM-DD)
- `start_date_to` (optional): Filter projects starting up to date (YYYY-MM-DD)
- `name` (optional): Search by name (partial match, case-insensitive)
- `limit` (optional): Max results (1-100, default: 20)
- `offset` (optional): Skip results (default: 0)

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Downtown Office Complex",
      "description": "Construction of 15-story office building",
      "status": "active",
      "budget": 5500000.00,
      "start_date": "2026-03-01",
      "end_date": "2027-12-31",
      "created_at": "2026-02-12T10:30:00Z",
      "updated_at": "2026-02-12T10:30:00Z"
    }
  ],
  "total": 1,
  "limit": 20,
  "offset": 0
}
```

#### 2. Create Project
```
POST /api/projects
```

**Request Body:**
```json
{
  "name": "Downtown Office Complex",          // Required, 1-200 chars
  "description": "15-story office building",  // Optional, max 2000 chars
  "status": "active",                         // Optional, default: "active"
  "budget": 5500000.00,                       // Optional, >= 0
  "start_date": "2026-03-01",                 // Required, YYYY-MM-DD
  "end_date": "2027-12-31"                    // Optional, YYYY-MM-DD
}
```

**Response (201):**
Returns `ProjectRead` object with generated `id`, `created_at`, `updated_at`.

#### 3. Get Project by ID
```
GET /api/projects/{id}
```

**Response (200):**
Returns `ProjectRead` object.

**Response (404):**
```json
{
  "detail": "Project not found"
}
```

#### 4. Update Project
```
PUT /api/projects/{id}
```

**Request Body (all fields optional):**
```json
{
  "name": "Updated Project Name",
  "status": "completed",
  "end_date": "2027-11-15"
}
```

**Response (200):**
Returns updated `ProjectRead` object.

#### 5. Delete Project
```
DELETE /api/projects/{id}
```

**Response (204):**
No content. Project and all associated locations are deleted.

---

### Locations

#### 6. List Project Locations
```
GET /api/projects/{id}/locations
```

**Response (200):**
```json
[
  {
    "id": 1,
    "project_id": 1,
    "name": "Main Construction Site",
    "address": "123 Broadway, New York, NY 10001",
    "coordinates": {
      "lat": 40.7128,
      "lng": -74.0060
    },
    "notes": "Primary excavation site",
    "created_at": "2026-02-12T10:35:00Z",
    "updated_at": "2026-02-12T10:35:00Z"
  }
]
```

#### 7. Add Location to Project
```
POST /api/projects/{id}/locations
```

**Request Body:**
```json
{
  "name": "Main Construction Site",           // Required, 1-200 chars
  "address": "123 Broadway, NY 10001",        // Required, 1-500 chars
  "coordinates": {                            // Optional
    "lat": 40.7128,
    "lng": -74.0060
  },
  "notes": "Primary excavation site"          // Optional, max 2000 chars
}
```

**Response (201):**
Returns `LocationRead` object with generated `id`, `project_id`, `created_at`, `updated_at`.

#### 8. Update Location
```
PUT /api/locations/{id}
```

**Request Body (all fields optional):**
```json
{
  "notes": "Excavation completed, foundation work in progress"
}
```

**Response (200):**
Returns updated `LocationRead` object.

#### 9. Delete Location
```
DELETE /api/locations/{id}
```

**Response (204):**
No content. Location is permanently deleted.

---

## Error Responses

### Simple Error
```json
{
  "detail": "Project not found"
}
```

### Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "name"],
      "msg": "field required",
      "type": "value_error.missing"
    },
    {
      "loc": ["body", "budget"],
      "msg": "ensure this value is greater than or equal to 0",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

## Validation Rules

### Project
- **name**: Required, 1-200 characters
- **description**: Optional, max 2000 characters
- **status**: Optional, must be one of: active, completed, on-hold (default: active)
- **budget**: Optional, must be >= 0
- **start_date**: Required, valid date in YYYY-MM-DD format
- **end_date**: Optional, valid date in YYYY-MM-DD format

### Location
- **name**: Required, 1-200 characters
- **address**: Required, 1-500 characters
- **coordinates.lat**: Optional, must be between -90 and 90
- **coordinates.lng**: Optional, must be between -180 and 180
- **notes**: Optional, max 2000 characters

## Implementation Notes

### Database Relationships
- Projects have a one-to-many relationship with Locations
- Deleting a project will cascade delete all associated locations
- Foreign key constraint ensures location.project_id references valid project

### Pagination
- Default limit: 20 items
- Maximum limit: 100 items
- Use `offset` for page navigation: `?limit=20&offset=40` gets page 3

### Date Filtering
- Date ranges are inclusive on both ends
- Use ISO 8601 format: YYYY-MM-DD
- Example: `?start_date_from=2026-01-01&start_date_to=2026-12-31`

### Name Search
- Case-insensitive partial matching
- Searches within project name field
- Example: `?name=office` matches "Office Complex", "Home Office", etc.

### CORS
- API enables CORS for frontend integration
- Allowed origins: http://localhost:3000, http://Frontend:3000
- All HTTP methods and headers allowed

## Testing the API

### Using curl

**Create a project:**
```bash
curl -X POST http://localhost:8000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Project",
    "start_date": "2026-03-01"
  }'
```

**List projects:**
```bash
curl http://localhost:8000/api/projects?status=active&limit=10
```

**Add a location:**
```bash
curl -X POST http://localhost:8000/api/projects/1/locations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Site A",
    "address": "123 Main St"
  }'
```

### Using Python

```python
import requests

# Create project
response = requests.post(
    "http://localhost:8000/api/projects",
    json={
        "name": "My Project",
        "start_date": "2026-03-01"
    }
)
project = response.json()
print(f"Created project ID: {project['id']}")

# List projects with filters
response = requests.get(
    "http://localhost:8000/api/projects",
    params={"status": "active", "limit": 10}
)
projects = response.json()
print(f"Found {projects['total']} projects")
```

## TypeScript Types (for Frontend)

```typescript
export enum ProjectStatus {
  ACTIVE = "active",
  COMPLETED = "completed",
  ON_HOLD = "on-hold"
}

export interface Coordinates {
  lat: number;
  lng: number;
}

export interface Project {
  id: number;
  name: string;
  description?: string;
  status: ProjectStatus;
  budget?: number;
  start_date: string;
  end_date?: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectCreate {
  name: string;
  description?: string;
  status?: ProjectStatus;
  budget?: number;
  start_date: string;
  end_date?: string;
}

export interface ProjectUpdate {
  name?: string;
  description?: string;
  status?: ProjectStatus;
  budget?: number;
  start_date?: string;
  end_date?: string;
}

export interface Location {
  id: number;
  project_id: number;
  name: string;
  address: string;
  coordinates?: Coordinates;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface LocationCreate {
  name: string;
  address: string;
  coordinates?: Coordinates;
  notes?: string;
}

export interface LocationUpdate {
  name?: string;
  address?: string;
  coordinates?: Coordinates;
  notes?: string;
}

export interface ProjectListResponse {
  items: Project[];
  total: number;
  limit: number;
  offset: number;
}
```

## OpenAPI Specification

The complete OpenAPI 3.0 specification is available in `api-contract.json`.

You can:
- Import it into Postman/Insomnia for testing
- Generate client SDKs using OpenAPI Generator
- View interactive documentation at `/docs` (FastAPI automatic)
- View alternative documentation at `/redoc` (FastAPI automatic)
