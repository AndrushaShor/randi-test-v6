"""
Locations API endpoints
Handles CRUD operations for project locations
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, Project, Location
from app.schemas import LocationCreate, LocationUpdate, LocationRead

router = APIRouter()


@router.get("/projects/{project_id}/locations", response_model=List[LocationRead])
async def list_project_locations(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    List all locations for a specific project
    
    Returns:
    - Array of locations belonging to the project
    """
    # Verify project exists
    project_query = select(Project).where(Project.id == project_id)
    project_result = await db.execute(project_query)
    project = project_result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    # Get locations
    query = select(Location).where(Location.project_id == project_id)
    result = await db.execute(query)
    locations = result.scalars().all()
    
    return [LocationRead.model_validate(loc) for loc in locations]


@router.post("/projects/{project_id}/locations", response_model=LocationRead, status_code=status.HTTP_201_CREATED)
async def create_location(
    project_id: UUID,
    location_data: LocationCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Add a new location to a project
    
    Required fields:
    - name: Location name
    - address: Physical address
    
    Optional fields:
    - coordinates: GPS coordinates (lat/lng)
    - notes: Additional notes
    """
    # Verify project exists
    project_query = select(Project).where(Project.id == project_id)
    project_result = await db.execute(project_query)
    project = project_result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    # Create location
    location_dict = location_data.model_dump()
    
    # Handle coordinates
    coordinates = location_dict.pop('coordinates', None)
    if coordinates:
        location_dict['latitude'] = coordinates.get('lat')
        location_dict['longitude'] = coordinates.get('lng')
    
    location = Location(project_id=project_id, **location_dict)
    db.add(location)
    await db.commit()
    await db.refresh(location)
    
    return LocationRead.model_validate(location)


@router.put("/locations/{location_id}", response_model=LocationRead)
async def update_location(
    location_id: UUID,
    location_data: LocationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing location
    
    All fields are optional. Only provided fields will be updated.
    """
    # Get existing location
    query = select(Location).where(Location.id == location_id)
    result = await db.execute(query)
    location = result.scalar_one_or_none()
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    
    # Update fields
    update_data = location_data.model_dump(exclude_unset=True)
    
    # Handle coordinates
    coordinates = update_data.pop('coordinates', None)
    if coordinates:
        update_data['latitude'] = coordinates.get('lat')
        update_data['longitude'] = coordinates.get('lng')
    
    for field, value in update_data.items():
        setattr(location, field, value)
    
    await db.commit()
    await db.refresh(location)
    
    return LocationRead.model_validate(location)


@router.delete("/locations/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a location
    """
    query = select(Location).where(Location.id == location_id)
    result = await db.execute(query)
    location = result.scalar_one_or_none()
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    
    await db.delete(location)
    await db.commit()
    
    return None
