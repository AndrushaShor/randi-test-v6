# Data Engineering

## Overview

The Data Engineering team designed and implemented a normalized PostgreSQL database schema for a construction project management system. The schema supports Projects and Locations entities with a 1:N relationship (one project has many locations), complete with proper foreign key constraints, performance indexes, and fully reversible Alembic migrations.

## Architecture

### Database Design

**Schema Model**: Normalized 3NF (Third Normal Form)

**Tables**:
- `projects` - Main project records with metadata, budget, and timeline
- `locations` - Physical locations associated with each project

**Relationship**: 
- Projects 1:N Locations (one-to-many)
- Foreign key with CASCADE delete (deleting a project removes all its locations)

**Technology Stack**:
- PostgreSQL 16+
- SQLAlchemy 2.0 (ORM)
- Alembic 1.18 (migrations)
- psycopg2-binary (database adapter)

### File Structure

```
db/
├── __init__.py                    # Package initialization
├── models.py                       # SQLAlchemy ORM models
├── connection.py                   # Database connection utilities
├── schema.sql                      # SQL schema documentation
├── SCHEMA.md                       # Schema documentation
└── requirements.txt                # Python dependencies

alembic/
├── alembic.ini                     # Alembic configuration
├── env.py                          # Alembic environment setup
└── versions/
    └── 2d4ebf6ab1f7_*.py          # Initial migration (create tables)

test_db_connection.py               # Comprehensive database tests
```

## Setup & Running

### Prerequisites

- PostgreSQL database accessible at `postgres:5432`
- Python 3.12+
- pip package manager

### Installation

```bash
# Install Python dependencies
pip install -r db/requirements.txt

# Or install individually
pip install psycopg2-binary sqlalchemy alembic
```

### Database Connection

**Connection Details**:
```
Host: postgres
Port: 5432
Database: appdb
User: agent
Password: agent_dev
Connection String: postgresql://agent:agent_dev@postgres:5432/appdb
```

### Apply Migrations

```bash
# Add alembic to PATH
export PATH="/home/agent/.local/bin:$PATH"

# Apply all migrations (create tables)
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback all migrations
alembic downgrade base

# Check current migration status
alembic current

# View migration history
alembic history
```

### Run Tests

```bash
# Run comprehensive database tests
python3 test_db_connection.py
```

Tests verify:
- Database connectivity
- Project and Location CRUD operations
- Relationship queries
- Index performance
- CASCADE delete behavior

## API / Interfaces

### SQLAlchemy Models

Located in `db/models.py`:

```python
from db.models import Project, Location
from db.connection import get_db

# Get database session
db = next(get_db())

# Create a project
project = Project(
    name="New Construction Project",
    status="active",
    start_date=date(2026, 3, 1),
    budget=Decimal("500000.00")
)
db.add(project)
db.commit()

# Create a location
location = Location(
    project_id=project.id,
    name="Main Office",
    address="123 Construction Ave",
    latitude=Decimal("37.7749"),
    longitude=Decimal("-122.4194")
)
db.add(location)
db.commit()

# Query with relationships
project_with_locations = db.query(Project).filter(
    Project.id == project_id
).first()
print(f"Locations: {len(project_with_locations.locations)}")
```

### Database Schema

#### Projects Table

| Column | Type | Constraints | Index |
|--------|------|-------------|-------|
| id | UUID | PRIMARY KEY | - |
| name | VARCHAR(255) | NOT NULL | ✅ (search) |
| status | VARCHAR(50) | nullable | ✅ (filter) |
| start_date | DATE | NOT NULL | ✅ (composite) |
| end_date | DATE | nullable | ✅ (composite) |
| budget | DECIMAL(15,2) | nullable | - |
| description | TEXT | nullable | - |
| created_at | TIMESTAMP WITH TIMEZONE | NOT NULL, DEFAULT NOW() | - |
| updated_at | TIMESTAMP WITH TIMEZONE | NOT NULL, DEFAULT NOW() | - |

**Indexes**:
- `idx_projects_name` - B-tree index on `name` for fast search
- `idx_projects_status` - B-tree index on `status` for filtering
- `idx_projects_dates` - Composite index on `(start_date, end_date)` for date range queries

#### Locations Table

| Column | Type | Constraints | Index |
|--------|------|-------------|-------|
| id | UUID | PRIMARY KEY | - |
| project_id | UUID | NOT NULL, FK → projects.id | ✅ |
| name | VARCHAR(255) | NOT NULL | - |
| address | VARCHAR(500) | nullable | - |
| latitude | DECIMAL(10,8) | nullable | - |
| longitude | DECIMAL(11,8) | nullable | - |
| notes | TEXT | nullable | - |
| created_at | TIMESTAMP WITH TIMEZONE | NOT NULL, DEFAULT NOW() | - |
| updated_at | TIMESTAMP WITH TIMEZONE | NOT NULL, DEFAULT NOW() | - |

**Foreign Key**:
- `fk_locations_project_id`: `locations.project_id` → `projects.id` with `ON DELETE CASCADE`

**Index**:
- `idx_locations_project_id` - B-tree index on `project_id` for foreign key lookups

### Connection Utilities

Located in `db/connection.py`:

```python
from db.connection import get_db, init_db

# Initialize database connection (call once at startup)
init_db()

# Use in FastAPI dependency injection
from fastapi import Depends
from sqlalchemy.orm import Session

@app.get("/api/projects")
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()
```

### Backend Team Integration

The complete schema contract is available in `.hive/messages/data-engineering-schema-contract.json` with:
- Full table definitions
- Column types and constraints
- Index specifications
- Foreign key relationships
- SQLAlchemy model imports
- Connection utility usage
- Pydantic model suggestions
- Example CRUD operations

## Key Decisions

### 1. UUID Primary Keys
**Decision**: Use UUID v4 for all primary keys instead of auto-incrementing integers.

**Rationale**:
- Globally unique identifiers enable distributed systems and data merges
- No sequential ID leakage concerns
- Better for public-facing APIs (harder to enumerate resources)
- PostgreSQL `gen_random_uuid()` provides efficient native support

### 2. Timestamp Columns
**Decision**: Include `created_at` and `updated_at` on all tables with `TIMESTAMP WITH TIMEZONE` type.

**Rationale**:
- Audit trail for when records were created and last modified
- Essential for debugging data issues
- Timezone awareness prevents ambiguity in multi-region deployments
- Automatic defaults via `server_default=text('CURRENT_TIMESTAMP')`

### 3. ON DELETE CASCADE
**Decision**: Use `ON DELETE CASCADE` for the `locations.project_id` foreign key.

**Rationale**:
- Locations are meaningless without their parent project
- Prevents orphaned location records
- Simplifies project deletion logic (no need to manually clean up locations)
- Standard pattern for dependent child records

### 4. Decimal Type for Money
**Decision**: Use `DECIMAL(15,2)` for the `budget` field instead of FLOAT.

**Rationale**:
- Exact precision for financial calculations (no floating-point errors)
- Supports budgets up to $999,999,999,999.99
- Standard practice for monetary values in databases

### 5. Decimal Type for Coordinates
**Decision**: Use `DECIMAL(10,8)` for latitude and `DECIMAL(11,8)` for longitude.

**Rationale**:
- Precision: 8 decimal places provides accuracy to ~1mm
- Latitude range: -90.00000000 to 90.00000000
- Longitude range: -180.00000000 to 180.00000000
- Avoids floating-point precision issues for geospatial data

### 6. Performance Indexes
**Decision**: Create indexes on `projects.name`, `projects.status`, and `locations.project_id`.

**Rationale**:
- `name` index: Supports fast text search queries (common use case: find projects by name)
- `status` index: Enables efficient filtering by project status (active, completed, on-hold)
- `project_id` index: Optimizes foreign key lookups and JOIN operations (critical for 1:N relationship queries)
- Composite `(start_date, end_date)` index: Supports date range queries

### 7. Nullable vs NOT NULL
**Decision**: Only require `name` and `start_date` as NOT NULL for projects; require `name` for locations.

**Rationale**:
- Minimizes data entry friction (users can create draft projects)
- End date may be unknown at project creation time
- Budget might be estimated later in the planning phase
- Flexible schema allows for progressive data refinement

### 8. Alembic Over create_all()
**Decision**: Use Alembic migrations exclusively instead of SQLAlchemy's `create_all()`.

**Rationale**:
- Version-controlled schema changes
- Reversible migrations (upgrade and downgrade paths)
- Safe for production deployments
- Enables zero-downtime schema migrations
- Tracks migration history in `alembic_version` table

### 9. SQLAlchemy 2.0 Mapped[] Type Annotations
**Decision**: Use SQLAlchemy 2.0's `Mapped[Type]` syntax for model attributes.

**Rationale**:
- Type safety: Full IDE autocomplete and type checking support
- Explicit nullability: `Mapped[str]` vs `Mapped[Optional[str]]`
- Modern SQLAlchemy best practice (2.0+ style)
- Better integration with tools like mypy and Pylance

### 10. Relationship Configuration
**Decision**: Define bidirectional relationships with `back_populates` and cascade options.

**Rationale**:
- `project.locations` provides easy access to all locations for a project
- `location.project` enables reverse navigation
- `cascade="all, delete-orphan"` on ORM level ensures in-memory consistency
- Simplifies application code (no manual relationship management)

## Testing Results

All database tests passed successfully:

✅ **Database Connection**: PostgreSQL connection established  
✅ **Project Creation**: INSERT operations working correctly  
✅ **Location Creation**: Foreign key relationships functioning  
✅ **Relationship Queries**: Bidirectional navigation working  
✅ **Index Performance**: Name search, status filter, and FK lookups optimized  
✅ **CASCADE Delete**: Deleting projects removes associated locations  

**Test Coverage**:
- Connection initialization
- CRUD operations (Create, Read, Update, Delete)
- Foreign key constraints
- Relationship queries
- Index utilization
- CASCADE delete behavior
- Data type validation
- Timestamp auto-generation

See `test_db_connection.py` for full test implementation.

## Migration History

### Initial Migration (2d4ebf6ab1f7)
**Created**: 2026-02-12  
**Description**: Create projects and locations tables

**Changes**:
- Created `projects` table with all columns
- Created `locations` table with all columns
- Added indexes: `idx_projects_name`, `idx_projects_status`, `idx_projects_dates`, `idx_locations_project_id`
- Added foreign key: `fk_locations_project_id` with CASCADE delete
- Added UUID primary keys on both tables
- Added timestamp columns with automatic defaults

**Reversible**: Yes (downgrade drops both tables)

## Documentation for Backend Team

The Backend team can find comprehensive integration documentation in:

1. **`.hive/messages/data-engineering-schema-contract.json`** - Complete schema contract with:
   - Full table structures
   - Column types and constraints
   - Index definitions
   - Foreign key relationships
   - SQLAlchemy model usage examples
   - Connection utility functions
   - Pydantic model suggestions for API validation

2. **`db/SCHEMA.md`** - Detailed schema documentation with:
   - Entity-Relationship Diagram (ERD)
   - Table definitions
   - Usage examples
   - Query patterns
   - Migration commands

3. **`db/models.py`** - SQLAlchemy ORM models ready for import

4. **`db/connection.py`** - Database session management utilities

## Performance Considerations

**Indexes**: Ensure queries use indexes by running `EXPLAIN ANALYZE`:
```sql
EXPLAIN ANALYZE SELECT * FROM projects WHERE name ILIKE '%Construction%';
EXPLAIN ANALYZE SELECT * FROM projects WHERE status = 'active';
EXPLAIN ANALYZE SELECT * FROM locations WHERE project_id = 'uuid-value';
```

**Connection Pooling**: SQLAlchemy's connection pool is configured with:
- Pool size: 5 connections
- Max overflow: 10 additional connections
- Pool recycle: 3600 seconds (1 hour)

**Query Optimization**:
- Use indexed columns in WHERE clauses
- Leverage relationship loading strategies (`selectinload`, `joinedload`)
- Avoid N+1 queries when fetching projects with locations

## Security Notes

**Credentials**: Database credentials are stored in environment variables and `.git-credentials` (container-only, not committed to repository).

**SQL Injection**: All queries use SQLAlchemy's parameterized queries (no raw SQL string concatenation).

**Connection String**: The connection string is documented for backend integration but should be secured via environment variables in production.

## Next Steps for Backend Team

1. ✅ Install dependencies: `pip install -r db/requirements.txt`
2. ✅ Apply migrations: `alembic upgrade head`
3. ✅ Import models: `from db.models import Project, Location`
4. ✅ Use connection utilities: `from db.connection import get_db`
5. ✅ Implement FastAPI endpoints with SQLAlchemy queries
6. ✅ Add Pydantic models for request/response validation
7. ✅ Test CRUD operations with the database

See `.hive/messages/data-engineering-schema-contract.json` for detailed integration instructions.

---

**Contact**: Data Engineering Team  
**Status**: ✅ Complete and tested  
**Database**: Ready for Backend integration  
**Last Updated**: 2026-02-12
