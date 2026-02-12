# Database Models & Connection

SQLAlchemy 2.0 async ORM models and database connection utilities for the Construction Project Management API.

## Overview

This package provides:
- **SQLAlchemy 2.0 async models** for Projects and Locations
- **Async database connection utilities** with PostgreSQL
- **FastAPI dependency injection** for database sessions
- **Proper indexing** for query performance
- **CASCADE delete** for referential integrity

## Database Schema

### Projects Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique project identifier (auto-generated) |
| `name` | VARCHAR(255) | NOT NULL, INDEXED | Project name (indexed for search) |
| `status` | VARCHAR(50) | NULL, INDEXED | Project status (planning, active, completed, archived) |
| `start_date` | DATE | NOT NULL | Project start date |
| `end_date` | DATE | NULL | Project end date (NULL if ongoing) |
| `budget` | DECIMAL(15,2) | NULL | Project budget in currency units |
| `description` | TEXT | NULL | Detailed project description |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record update timestamp (auto-updated) |

**Indexes:**
- `ix_projects_name` - B-tree index on `name` for fast search
- `ix_projects_status` - B-tree index on `status` for filtering
- `idx_projects_dates` - Composite index on `(start_date, end_date)` for date range queries

**Relationship:**
- Has many `Locations` (1:N relationship with CASCADE delete)

### Locations Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique location identifier (auto-generated) |
| `project_id` | UUID | FOREIGN KEY, NOT NULL, INDEXED | Reference to parent project |
| `name` | VARCHAR(255) | NOT NULL | Location name |
| `address` | VARCHAR(500) | NULL | Physical address |
| `latitude` | DECIMAL(10,8) | NULL | Latitude coordinate (WGS84) |
| `longitude` | DECIMAL(11,8) | NULL | Longitude coordinate (WGS84) |
| `notes` | TEXT | NULL | Additional location notes |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Record update timestamp (auto-updated) |

**Indexes:**
- `ix_locations_project_id` - B-tree index on `project_id` for JOIN performance

**Foreign Keys:**
- `project_id` → `projects.id` (CASCADE delete via SQLAlchemy relationship)

## Usage

### Import Models

```python
from app.database import Base, Project, Location, get_db, init_db
```

### Initialize Database (Development Only)

```python
import asyncio
from app.database import init_db

async def setup():
    await init_db()  # Creates all tables

asyncio.run(setup())
```

**Note:** In production, use Alembic migrations instead of `init_db()`.

### FastAPI Endpoint with Database Session

```python
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db, Project

@app.get("/api/projects")
async def get_projects(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects
```

### Query Examples

#### Select all projects
```python
from sqlalchemy import select
from app.database import Project

async with AsyncSessionLocal() as session:
    result = await session.execute(select(Project))
    projects = result.scalars().all()
```

#### Select project by ID
```python
from sqlalchemy import select
from app.database import Project

async with AsyncSessionLocal() as session:
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
```

#### Select project with locations (eager loading)
```python
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import Project

async with AsyncSessionLocal() as session:
    result = await session.execute(
        select(Project)
        .options(selectinload(Project.locations))
        .where(Project.id == project_id)
    )
    project = result.scalar_one_or_none()
    # project.locations is now loaded
```

#### Create project
```python
from datetime import date
from uuid import uuid4
from app.database import Project

async with AsyncSessionLocal() as session:
    project = Project(
        id=uuid4(),
        name="New Project",
        status="planning",
        start_date=date(2024, 1, 1),
        budget=100000.00,
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)
```

#### Create location for project
```python
from uuid import uuid4
from app.database import Location

async with AsyncSessionLocal() as session:
    location = Location(
        id=uuid4(),
        project_id=project_id,
        name="Site A",
        address="123 Main St",
        latitude=37.7749,
        longitude=-122.4194,
    )
    session.add(location)
    await session.commit()
```

#### Update project
```python
from sqlalchemy import select
from app.database import Project

async with AsyncSessionLocal() as session:
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one()
    project.status = "active"
    await session.commit()
```

#### Delete project (cascades to locations)
```python
from sqlalchemy import select
from app.database import Project

async with AsyncSessionLocal() as session:
    result = await session.execute(
        select(Project).where(Project.id == project_id)
    )
    project = result.scalar_one()
    await session.delete(project)
    await session.commit()
    # All associated locations are automatically deleted
```

## Connection Configuration

Database connection string is configured in `app/core/config.py`:

```python
DATABASE_URL: str = "postgresql://agent:agent_dev@postgres:5432/appdb"
```

The connection module automatically converts this to the async driver:
```python
postgresql+asyncpg://agent:agent_dev@postgres:5432/appdb
```

### Connection Pool Settings

- **Pool size:** 5 connections
- **Max overflow:** 10 additional connections
- **Pre-ping:** Enabled (verifies connections before use)
- **Echo:** Disabled (set to `True` for SQL query logging)

## Files

- `app/database/__init__.py` - Package exports
- `app/database/models.py` - SQLAlchemy ORM models (Project, Location)
- `app/database/connection.py` - Async engine, session factory, FastAPI dependency
- `app/database/README.md` - This documentation

## Dependencies

```
sqlalchemy==2.0.25  # ORM framework
asyncpg==0.29.0     # Async PostgreSQL driver
psycopg2-binary==2.9.9  # Sync PostgreSQL driver (for compatibility)
```

## Testing

Run the verification scripts:

```bash
# Test connection and table creation
python test_db_connection.py

# Verify schema structure
python verify_schema.py

# Test CASCADE delete behavior
python test_cascade_delete.py
```

## Notes

- All models use UUID primary keys with `uuid4()` defaults
- Timestamps (`created_at`, `updated_at`) are auto-managed
- The `updated_at` field automatically updates on record modification
- CASCADE delete is implemented via SQLAlchemy relationship, not database FK constraint
- All database operations are async using `AsyncSession`
- Use `Depends(get_db)` in FastAPI endpoints for automatic session management

## Next Steps

1. Create Pydantic schemas for API validation (see Data Engineering contract for suggestions)
2. Implement FastAPI endpoints using these models
3. Add Alembic migrations for production schema changes
4. Implement query filters (status, date range, name search)
5. Add pagination support for list endpoints
