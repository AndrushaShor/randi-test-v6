"""
Projects API endpoints
Handles CRUD operations for construction projects
"""
from typing import List, Optional
from datetime import date
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db, Project
from app.schemas import ProjectCreate, ProjectUpdate, ProjectRead, ProjectListResponse

router = APIRouter()


@router.get("/projects", response_model=ProjectListResponse)
async def list_projects(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status"),
    start_date_from: Optional[date] = Query(None, description="Filter by start date from"),
    start_date_to: Optional[date] = Query(None, description="Filter by start date to"),
    name: Optional[str] = Query(None, description="Search by project name"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    db: AsyncSession = Depends(get_db)
):
    """
    List all projects with optional filtering and pagination
    
    Query parameters:
    - status: Filter by project status (active, completed, on-hold)
    - start_date_from: Filter projects starting from this date
    - start_date_to: Filter projects starting before this date
    - name: Search by project name (partial match)
    - limit: Max number of results (default 100)
    - offset: Skip N results for pagination (default 0)
    """
    # Build query
    query = select(Project)
    
    # Apply filters
    if status_filter:
        query = query.where(Project.status == status_filter)
    
    if start_date_from:
        query = query.where(Project.start_date >= start_date_from)
    
    if start_date_to:
        query = query.where(Project.start_date <= start_date_to)
    
    if name:
        query = query.where(Project.name.ilike(f"%{name}%"))
    
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination
    query = query.offset(offset).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    projects = result.scalars().all()
    
    return ProjectListResponse(
        items=[ProjectRead.model_validate(p) for p in projects],
        total=total,
        limit=limit,
        offset=offset
    )


@router.post("/projects", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new project
    
    Required fields:
    - name: Project name (1-200 characters)
    - start_date: Project start date
    
    Optional fields:
    - description: Detailed description
    - status: active (default), completed, on-hold
    - budget: Project budget
    - end_date: Project end date
    """
    # Validate end_date is after start_date
    if project_data.end_date and project_data.end_date < project_data.start_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_date must be after start_date"
        )
    
    # Create project
    project = Project(**project_data.model_dump())
    db.add(project)
    await db.commit()
    await db.refresh(project)
    
    return ProjectRead.model_validate(project)


@router.get("/projects/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a single project by ID
    
    Returns:
    - Project details including all locations
    """
    query = select(Project).where(Project.id == project_id).options(selectinload(Project.locations))
    result = await db.execute(query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    return ProjectRead.model_validate(project)


@router.put("/projects/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: UUID,
    project_data: ProjectUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update an existing project
    
    All fields are optional. Only provided fields will be updated.
    """
    # Get existing project
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    # Update fields
    update_data = project_data.model_dump(exclude_unset=True)
    
    # Validate end_date if both dates are present
    new_start = update_data.get('start_date', project.start_date)
    new_end = update_data.get('end_date', project.end_date)
    if new_end and new_end < new_start:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_date must be after start_date"
        )
    
    for field, value in update_data.items():
        setattr(project, field, value)
    
    await db.commit()
    await db.refresh(project)
    
    return ProjectRead.model_validate(project)


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a project
    
    This will also delete all associated locations (CASCADE delete).
    """
    query = select(Project).where(Project.id == project_id)
    result = await db.execute(query)
    project = result.scalar_one_or_none()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with id {project_id} not found"
        )
    
    await db.delete(project)
    await db.commit()
    
    return None
