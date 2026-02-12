"""Test CASCADE delete behavior"""

import asyncio
from datetime import date
from uuid import uuid4
from sqlalchemy import select
from app.database.connection import init_db, AsyncSessionLocal
from app.database.models import Project, Location


async def test_cascade():
    """Test that deleting a project cascades to its locations"""
    
    await init_db()
    
    async with AsyncSessionLocal() as session:
        # Create a test project
        project = Project(
            id=uuid4(),
            name="Test Cascade Project",
            status="active",
            start_date=date(2024, 1, 1),
            budget=100000.00,
        )
        session.add(project)
        await session.flush()
        
        # Create locations for the project
        location1 = Location(
            id=uuid4(),
            project_id=project.id,
            name="Location 1",
            address="123 Main St",
        )
        location2 = Location(
            id=uuid4(),
            project_id=project.id,
            name="Location 2",
            address="456 Oak Ave",
        )
        session.add_all([location1, location2])
        await session.commit()
        
        project_id = project.id
        print(f"✅ Created project {project_id} with 2 locations")
        
    # Verify locations exist
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Location).where(Location.project_id == project_id)
        )
        locations = result.scalars().all()
        print(f"📍 Found {len(locations)} locations before delete")
        
    # Delete the project
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Project).where(Project.id == project_id)
        )
        project = result.scalar_one()
        await session.delete(project)
        await session.commit()
        print(f"🗑️  Deleted project {project_id}")
    
    # Check if locations were cascade deleted
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Location).where(Location.project_id == project_id)
        )
        locations = result.scalars().all()
        print(f"📍 Found {len(locations)} locations after delete")
        
        if len(locations) == 0:
            print("✅ CASCADE DELETE working correctly!")
        else:
            print("❌ CASCADE DELETE not working - orphaned locations remain")


if __name__ == "__main__":
    asyncio.run(test_cascade())
