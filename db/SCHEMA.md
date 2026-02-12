# Database Schema Documentation

## Overview

This database schema implements a **Projects and Locations** system with a **1:N relationship** (one Project has many Locations).

## Entity Relationship Diagram

```
┌─────────────────────────────┐
│        PROJECTS             │
├─────────────────────────────┤
│ id (UUID) PK                │
│ name (VARCHAR) NOT NULL ⚡  │
│ status (VARCHAR) ⚡         │
│ start_date (DATE) NOT NULL  │
│ end_date (DATE)             │
│ budget (DECIMAL)            │
│ description (TEXT)          │
│ created_at (TIMESTAMPTZ)    │
│ updated_at (TIMESTAMPTZ)    │
└─────────────────────────────┘
              │
              │ 1:N
              │
              ▼
┌─────────────────────────────┐
│        LOCATIONS            │
├─────────────────────────────┤
│ id (UUID) PK                │
│ project_id (UUID) FK ⚡     │
│ name (VARCHAR) NOT NULL     │
│ address (VARCHAR)           │
│ latitude (DECIMAL)          │
│ longitude (DECIMAL)         │
│ notes (TEXT)                │
│ created_at (TIMESTAMPTZ)    │
│ updated_at (TIMESTAMPTZ)    │
└─────────────────────────────┘

⚡ = Indexed for performance
```

## Tables

### Projects

Stores project metadata including timeline, budget, and status.

**Columns:**
- `id` (UUID, Primary Key) - Unique project identifier
- `name` (VARCHAR(255), NOT NULL, INDEXED) - Project name for display and search
- `status` (VARCHAR(50), INDEXED) - Project status (e.g., "planning", "active", "completed", "archived")
- `start_date` (DATE, NOT NULL) - Project start date
- `end_date` (DATE, NULLABLE) - Project end date (NULL if ongoing)
- `budget` (DECIMAL(15,2), NULLABLE) - Project budget in currency units
- `description` (TEXT, NULLABLE) - Detailed project description
- `created_at` (TIMESTAMP WITH TIME ZONE) - Record creation timestamp
- `updated_at` (TIMESTAMP WITH TIME ZONE) - Record last update timestamp

**Indexes:**
- `idx_projects_name` - B-tree index on `name` for fast search queries
- `idx_projects_status` - B-tree index on `status` for filtering
- `idx_projects_dates` - Composite index on `(start_date, end_date)` for date range queries

### Locations

Stores geographic locations associated with projects.

**Columns:**
- `id` (UUID, Primary Key) - Unique location identifier
- `project_id` (UUID, Foreign Key, NOT NULL, INDEXED) - References `projects.id`
- `name` (VARCHAR(255), NOT NULL) - Location name
- `address` (VARCHAR(500), NULLABLE) - Physical address
- `latitude` (DECIMAL(10,8), NULLABLE) - Latitude coordinate (WGS84)
- `longitude` (DECIMAL(11,8), NULLABLE) - Longitude coordinate (WGS84)
- `notes` (TEXT, NULLABLE) - Additional location notes
- `created_at` (TIMESTAMP WITH TIME ZONE) - Record creation timestamp
- `updated_at` (TIMESTAMP WITH TIME ZONE) - Record last update timestamp

**Indexes:**
- `idx_locations_project_id` - B-tree index on `project_id` for foreign key lookups

**Foreign Keys:**
- `fk_locations_project` - `project_id` → `projects.id` with `ON DELETE CASCADE`

## Relationships

### Projects → Locations (1:N)

- **Cardinality**: One Project can have many Locations
- **Foreign Key**: `locations.project_id` → `projects.id`
- **Delete Behavior**: `ON DELETE CASCADE` - When a project is deleted, all associated locations are automatically deleted

## Performance Considerations

### Indexes

1. **projects.name** - Supports fast text search queries like `WHERE name ILIKE '%search%'`
2. **projects.status** - Optimizes status filtering queries like `WHERE status = 'active'`
3. **projects.dates** - Composite index for date range queries
4. **locations.project_id** - Critical for JOIN performance and foreign key integrity

### Query Patterns

Optimized for:
- Project name search: `SELECT * FROM projects WHERE name ILIKE '%term%'`
- Status filtering: `SELECT * FROM projects WHERE status = 'active'`
- Date range queries: `SELECT * FROM projects WHERE start_date >= '2024-01-01' AND end_date <= '2024-12-31'`
- Location lookup by project: `SELECT * FROM locations WHERE project_id = $1`
- Projects with locations (JOIN): `SELECT p.*, l.* FROM projects p LEFT JOIN locations l ON p.id = l.project_id`

## Data Types

### UUID
- Primary keys use UUID v4 for global uniqueness
- Generated using `uuid_generate_v4()` in PostgreSQL or `uuid.uuid4()` in Python

### Timestamps
- All timestamps use `TIMESTAMP WITH TIME ZONE` for timezone-aware storage
- `created_at` defaults to `CURRENT_TIMESTAMP`
- `updated_at` automatically updates on record modification

### Decimal
- Budget: `DECIMAL(15,2)` - Up to 13 digits before decimal, 2 after (e.g., $9,999,999,999,999.99)
- Latitude: `DECIMAL(10,8)` - Range: -90.00000000 to 90.00000000
- Longitude: `DECIMAL(11,8)` - Range: -180.00000000 to 180.00000000

## Connection Information

### Local PostgreSQL Instance

```
Host: postgres (or $DB_HOST)
Port: 5432
Database: appdb
User: agent
Password: agent_dev
Connection String: postgresql://agent:agent_dev@postgres:5432/appdb
```

### Environment Variables

- `DB_HOST` - Database host (default: "postgres")
- `DB_PORT` - Database port (default: "5432")
- `DB_NAME` - Database name (default: "appdb")
- `DB_USER` - Database user (default: "agent")
- `DB_PASSWORD` - Database password (default: "agent_dev")

## Usage Examples

### Using SQLAlchemy Models

```python
from db.models import Project, Location
from db.connection import SessionLocal
from datetime import date
from decimal import Decimal

# Create a session
db = SessionLocal()

# Create a new project
project = Project(
    name="Downtown Renovation",
    status="planning",
    start_date=date(2024, 1, 1),
    budget=Decimal("500000.00"),
    description="Major downtown area renovation project"
)
db.add(project)
db.commit()
db.refresh(project)

# Add locations to the project
location1 = Location(
    project_id=project.id,
    name="Main Street Site",
    address="123 Main St, City, State",
    latitude=Decimal("40.7128"),
    longitude=Decimal("-74.0060"),
    notes="Primary construction site"
)
location2 = Location(
    project_id=project.id,
    name="Park Avenue Site",
    address="456 Park Ave, City, State",
    latitude=Decimal("40.7589"),
    longitude=Decimal("-73.9851")
)
db.add_all([location1, location2])
db.commit()

# Query projects with their locations
projects = db.query(Project).filter(Project.status == "active").all()
for p in projects:
    print(f"Project: {p.name}")
    for loc in p.locations:
        print(f"  - Location: {loc.name} at {loc.address}")

db.close()
```

### Direct SQL

```sql
-- Create a new project
INSERT INTO projects (name, status, start_date, budget, description)
VALUES ('Downtown Renovation', 'planning', '2024-01-01', 500000.00, 'Major downtown area renovation project');

-- Add locations
INSERT INTO locations (project_id, name, address, latitude, longitude, notes)
VALUES 
  ('project-uuid-here', 'Main Street Site', '123 Main St', 40.7128, -74.0060, 'Primary construction site'),
  ('project-uuid-here', 'Park Avenue Site', '456 Park Ave', 40.7589, -73.9851, NULL);

-- Query projects with location count
SELECT p.id, p.name, p.status, COUNT(l.id) as location_count
FROM projects p
LEFT JOIN locations l ON p.id = l.project_id
GROUP BY p.id, p.name, p.status;

-- Search projects by name
SELECT * FROM projects WHERE name ILIKE '%renovation%';

-- Filter by status
SELECT * FROM projects WHERE status = 'active';
```

## Normalization

This schema follows **Third Normal Form (3NF)**:

1. **1NF**: All columns contain atomic values (no arrays or nested structures)
2. **2NF**: No partial dependencies (all non-key columns depend on entire primary key)
3. **3NF**: No transitive dependencies (no non-key column depends on another non-key column)

The 1:N relationship between Projects and Locations eliminates data redundancy and ensures data integrity through foreign key constraints.

## File Structure

```
db/
├── __init__.py          # Package initialization
├── models.py            # SQLAlchemy ORM models
├── connection.py        # Database connection utilities
├── schema.sql           # SQL schema definition
└── SCHEMA.md           # This documentation file
```
