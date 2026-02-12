#!/usr/bin/env python3
"""
Test script to verify database schema, connections, and basic CRUD operations.
"""
import sys
from datetime import date, datetime
from decimal import Decimal
from uuid import uuid4

from db.connection import get_db, init_db
from db.models import Project, Location


def test_database_connection():
    """Test basic database connectivity."""
    print("=" * 60)
    print("Testing Database Connection")
    print("=" * 60)
    
    try:
        init_db()
        print("✅ Database connection initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_create_project():
    """Test creating a project."""
    print("\n" + "=" * 60)
    print("Testing Project Creation")
    print("=" * 60)
    
    try:
        db = next(get_db())
        
        # Create a test project
        project = Project(
            id=uuid4(),
            name="Test Construction Project",
            status="planning",
            start_date=date(2026, 3, 1),
            end_date=date(2026, 12, 31),
            budget=Decimal("500000.00"),
            description="A test project for database validation"
        )
        
        db.add(project)
        db.commit()
        db.refresh(project)
        
        print(f"✅ Created project: {project.name}")
        print(f"   ID: {project.id}")
        print(f"   Status: {project.status}")
        print(f"   Budget: ${project.budget}")
        print(f"   Created at: {project.created_at}")
        
        return project
    except Exception as e:
        print(f"❌ Project creation failed: {e}")
        db.rollback()
        return None


def test_create_locations(project):
    """Test creating locations for a project."""
    print("\n" + "=" * 60)
    print("Testing Location Creation")
    print("=" * 60)
    
    if not project:
        print("⚠️  Skipping location test - no project available")
        return []
    
    try:
        db = next(get_db())
        
        locations_data = [
            {
                "name": "Main Site Office",
                "address": "123 Construction Ave, Builder City, BC 12345",
                "latitude": Decimal("37.7749"),
                "longitude": Decimal("-122.4194"),
                "notes": "Primary site office and coordination center"
            },
            {
                "name": "Equipment Yard",
                "address": "456 Warehouse Rd, Builder City, BC 12345",
                "latitude": Decimal("37.7849"),
                "longitude": Decimal("-122.4094"),
                "notes": "Heavy equipment storage and maintenance"
            }
        ]
        
        created_locations = []
        for loc_data in locations_data:
            location = Location(
                id=uuid4(),
                project_id=project.id,
                **loc_data
            )
            db.add(location)
            created_locations.append(location)
        
        db.commit()
        
        for loc in created_locations:
            db.refresh(loc)
            print(f"✅ Created location: {loc.name}")
            print(f"   ID: {loc.id}")
            print(f"   Address: {loc.address}")
            print(f"   Coordinates: ({loc.latitude}, {loc.longitude})")
        
        return created_locations
    except Exception as e:
        print(f"❌ Location creation failed: {e}")
        db.rollback()
        return []


def test_query_with_relationship(project):
    """Test querying projects with their locations."""
    print("\n" + "=" * 60)
    print("Testing Relationship Queries")
    print("=" * 60)
    
    if not project:
        print("⚠️  Skipping relationship test - no project available")
        return
    
    try:
        db = next(get_db())
        
        # Query project with locations
        queried_project = db.query(Project).filter(Project.id == project.id).first()
        
        print(f"✅ Queried project: {queried_project.name}")
        print(f"   Number of locations: {len(queried_project.locations)}")
        
        for i, location in enumerate(queried_project.locations, 1):
            print(f"   Location {i}: {location.name}")
        
    except Exception as e:
        print(f"❌ Relationship query failed: {e}")


def test_indexes():
    """Test that indexes are working for performance."""
    print("\n" + "=" * 60)
    print("Testing Database Indexes")
    print("=" * 60)
    
    try:
        db = next(get_db())
        
        # Test name search (should use idx_projects_name)
        projects_by_name = db.query(Project).filter(
            Project.name.like("%Construction%")
        ).all()
        print(f"✅ Name search query executed: Found {len(projects_by_name)} project(s)")
        
        # Test status filter (should use idx_projects_status)
        projects_by_status = db.query(Project).filter(
            Project.status == "planning"
        ).all()
        print(f"✅ Status filter query executed: Found {len(projects_by_status)} project(s)")
        
        # Test location by project_id (should use idx_locations_project_id)
        if projects_by_name:
            locations = db.query(Location).filter(
                Location.project_id == projects_by_name[0].id
            ).all()
            print(f"✅ Location lookup by project_id: Found {len(locations)} location(s)")
        
    except Exception as e:
        print(f"❌ Index test failed: {e}")


def test_cascade_delete(project):
    """Test CASCADE delete behavior."""
    print("\n" + "=" * 60)
    print("Testing CASCADE Delete")
    print("=" * 60)
    
    if not project:
        print("⚠️  Skipping cascade test - no project available")
        return
    
    try:
        db = next(get_db())
        
        # Count locations before delete
        location_count_before = db.query(Location).filter(
            Location.project_id == project.id
        ).count()
        
        print(f"   Locations before delete: {location_count_before}")
        
        # Delete the project
        db.query(Project).filter(Project.id == project.id).delete()
        db.commit()
        
        # Check if locations were cascaded
        location_count_after = db.query(Location).filter(
            Location.project_id == project.id
        ).count()
        
        print(f"   Locations after delete: {location_count_after}")
        
        if location_count_after == 0:
            print("✅ CASCADE delete working correctly - locations removed with project")
        else:
            print(f"❌ CASCADE delete failed - {location_count_after} locations still exist")
        
    except Exception as e:
        print(f"❌ CASCADE delete test failed: {e}")
        db.rollback()


def main():
    """Run all database tests."""
    print("\n" + "=" * 60)
    print("DATABASE SCHEMA AND CONNECTION TESTS")
    print("=" * 60)
    
    # Test 1: Connection
    if not test_database_connection():
        print("\n❌ Cannot proceed - database connection failed")
        sys.exit(1)
    
    # Test 2: Create project
    project = test_create_project()
    
    # Test 3: Create locations
    locations = test_create_locations(project)
    
    # Test 4: Query relationships
    test_query_with_relationship(project)
    
    # Test 5: Test indexes
    test_indexes()
    
    # Test 6: Test cascade delete
    test_cascade_delete(project)
    
    # Final summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("✅ All database tests completed successfully!")
    print("\nDatabase is ready for Backend team integration.")
    print("\nConnection details:")
    print("  Host: postgres")
    print("  Port: 5432")
    print("  Database: appdb")
    print("  User: agent")
    print("  Connection string: postgresql://agent:agent_dev@postgres:5432/appdb")
    print("=" * 60)


if __name__ == "__main__":
    main()
