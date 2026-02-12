"""
Pydantic schemas for Construction Project Management API
Auto-generated from api-contract.json OpenAPI specification
"""
from datetime import date, datetime
from typing import Optional, List
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field, ConfigDict


class ProjectStatus(str, Enum):
    """Project status enumeration"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ON_HOLD = "on-hold"


class Coordinates(BaseModel):
    """GPS coordinates model"""
    lat: float = Field(
        ...,
        ge=-90.0,
        le=90.0,
        description="Latitude coordinate"
    )
    lng: float = Field(
        ...,
        ge=-180.0,
        le=180.0,
        description="Longitude coordinate"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "lat": 40.7128,
                "lng": -74.0060
            }
        }
    )


# ==================== PROJECT SCHEMAS ====================

class ProjectCreate(BaseModel):
    """Schema for creating a new project"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Project name"
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Detailed project description"
    )
    status: ProjectStatus = Field(
        default=ProjectStatus.ACTIVE,
        description="Project status"
    )
    budget: Optional[float] = Field(
        None,
        ge=0.0,
        description="Project budget in dollars"
    )
    start_date: date = Field(
        ...,
        description="Project start date (YYYY-MM-DD)"
    )
    end_date: Optional[date] = Field(
        None,
        description="Project end date (YYYY-MM-DD)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Downtown Office Complex",
                "description": "Construction of 15-story office building in downtown district",
                "status": "active",
                "budget": 5500000.00,
                "start_date": "2026-03-01",
                "end_date": "2027-12-31"
            }
        }
    )


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project (all fields optional)"""
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Project name"
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Detailed project description"
    )
    status: Optional[ProjectStatus] = Field(
        None,
        description="Project status"
    )
    budget: Optional[float] = Field(
        None,
        ge=0.0,
        description="Project budget in dollars"
    )
    start_date: Optional[date] = Field(
        None,
        description="Project start date (YYYY-MM-DD)"
    )
    end_date: Optional[date] = Field(
        None,
        description="Project end date (YYYY-MM-DD)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "completed",
                "end_date": "2027-11-15"
            }
        }
    )


class ProjectRead(BaseModel):
    """Schema for reading project data"""
    id: UUID = Field(..., description="Unique project identifier")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Detailed project description")
    status: ProjectStatus = Field(..., description="Project status")
    budget: Optional[float] = Field(None, description="Project budget in dollars")
    start_date: date = Field(..., description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date")
    created_at: datetime = Field(..., description="Timestamp when project was created")
    updated_at: datetime = Field(..., description="Timestamp when project was last updated")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Downtown Office Complex",
                "description": "Construction of 15-story office building in downtown district",
                "status": "active",
                "budget": 5500000.00,
                "start_date": "2026-03-01",
                "end_date": "2027-12-31",
                "created_at": "2026-02-12T10:30:00Z",
                "updated_at": "2026-02-12T10:30:00Z"
            }
        }
    )


class ProjectListResponse(BaseModel):
    """Schema for paginated project list response"""
    items: List[ProjectRead] = Field(..., description="Array of projects")
    total: int = Field(..., description="Total number of projects matching filters")
    limit: int = Field(..., description="Maximum number of results returned")
    offset: int = Field(..., description="Number of results skipped")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
        }
    )


# ==================== LOCATION SCHEMAS ====================

class LocationCreate(BaseModel):
    """Schema for creating a new location"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Location name"
    )
    address: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Physical address of the location"
    )
    coordinates: Optional[Coordinates] = Field(
        None,
        description="GPS coordinates"
    )
    notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Additional notes about the location"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Main Construction Site",
                "address": "123 Broadway, New York, NY 10001",
                "coordinates": {
                    "lat": 40.7128,
                    "lng": -74.0060
                },
                "notes": "Primary excavation site"
            }
        }
    )


class LocationUpdate(BaseModel):
    """Schema for updating an existing location (all fields optional)"""
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Location name"
    )
    address: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="Physical address of the location"
    )
    coordinates: Optional[Coordinates] = Field(
        None,
        description="GPS coordinates"
    )
    notes: Optional[str] = Field(
        None,
        max_length=2000,
        description="Additional notes about the location"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "notes": "Excavation completed, foundation work in progress"
            }
        }
    )


class LocationRead(BaseModel):
    """Schema for reading location data"""
    id: UUID = Field(..., description="Unique location identifier")
    project_id: UUID = Field(..., description="ID of the parent project")
    name: str = Field(..., description="Location name")
    address: str = Field(..., description="Physical address of the location")
    coordinates: Optional[Coordinates] = Field(None, description="GPS coordinates")
    notes: Optional[str] = Field(None, description="Additional notes about the location")
    created_at: datetime = Field(..., description="Timestamp when location was created")
    updated_at: datetime = Field(..., description="Timestamp when location was last updated")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
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
        }
    )


# ==================== ERROR SCHEMAS ====================

class ValidationError(BaseModel):
    """Individual validation error detail"""
    loc: List[str] = Field(..., description="Location of the error")
    msg: str = Field(..., description="Error message")
    type: str = Field(..., description="Error type")


class ErrorResponse(BaseModel):
    """Standard error response schema"""
    detail: str | List[ValidationError] = Field(
        ...,
        description="Error message or list of validation errors"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"detail": "Project not found"},
                {
                    "detail": [
                        {
                            "loc": ["body", "name"],
                            "msg": "field required",
                            "type": "value_error.missing"
                        }
                    ]
                }
            ]
        }
    )
