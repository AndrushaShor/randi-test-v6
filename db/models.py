"""
SQLAlchemy models for Projects and Locations
"""
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    Column,
    String,
    Text,
    Date,
    DECIMAL,
    ForeignKey,
    DateTime,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for all models"""
    pass


class Project(Base):
    """
    Project model representing a project with metadata.
    
    Relationships:
        - One Project has many Locations (1:N)
    """
    __tablename__ = "projects"

    # Primary Key
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    # Core Fields
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True  # Indexed for search performance
    )
    status: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        index=True  # Indexed for filtering
    )
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True
    )
    budget: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 2),
        nullable=True
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    locations: Mapped[List["Location"]] = relationship(
        "Location",
        back_populates="project",
        cascade="all, delete-orphan",  # ON DELETE CASCADE behavior
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"


class Location(Base):
    """
    Location model representing a geographic location associated with a project.
    
    Relationships:
        - Many Locations belong to one Project (N:1)
    """
    __tablename__ = "locations"

    # Primary Key
    id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    # Foreign Key
    project_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True  # Indexed for foreign key lookups
    )

    # Core Fields
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    address: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    latitude: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(10, 8),
        nullable=True
    )
    longitude: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(11, 8),
        nullable=True
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Relationships
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="locations"
    )

    def __repr__(self) -> str:
        return f"<Location(id={self.id}, name='{self.name}', project_id={self.project_id})>"


# Additional indexes defined at module level for clarity
Index("idx_projects_dates", Project.start_date, Project.end_date)
