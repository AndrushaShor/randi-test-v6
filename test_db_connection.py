"""Test script to verify database connection and model setup"""

import asyncio
from sqlalchemy import select
from app.database.connection import init_db, AsyncSessionLocal
from app.database.models import Project, Location


async def test_connection():
    """Test database connection and create tables"""
    print("🔧 Initializing database tables...")
    await init_db()
    print("✅ Database tables created successfully!")
    
    # Test connection with a simple query
    print("\n🔍 Testing database connection...")
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Project))
        projects = result.scalars().all()
        print(f"✅ Connection successful! Found {len(projects)} projects in database.")
    
    print("\n📋 Model Summary:")
    print(f"  - Project model: {Project.__tablename__}")
    print(f"  - Location model: {Location.__tablename__}")
    print("\n🎉 All database tests passed!")


if __name__ == "__main__":
    asyncio.run(test_connection())
