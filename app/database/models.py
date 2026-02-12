"""SQLAlchemy 2.0 ORM models for Projects and Locations"""

from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID, uuid4

from sqlalchemy import (
    DECIMAL,
    Date,
    ForeignKey,
    Index,
    String,
    Text,
    TIMESTAMP,
    func,
)
from sqlalchemy.dialects.postgresql import UUID as PostgreSQLUUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models"""
    pass


class Project(Base):
    """Project ORM model
    
    Represents a construction project with metadata like name, status, dates, and budget.
    Has a 1:N relationship with Location.
    """
    
    __tablename__ = "projects"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    
    # Core fields
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,  # idx_projects_name
    )
    
    status: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        index=True,  # idx_projects_status
    )
    
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )
    
    end_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True,
    )
    
    budget: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(15, 2),
        nullable=True,
    )
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    # Relationships
    locations: Mapped[List["Location"]] = relationship(
        "Location",
        back_populates="project",
        cascade="all, delete-orphan",  # CASCADE delete
        lazy="selectin",
    )
    
    # Composite index for date range queries
    __table_args__ = (
        Index("idx_projects_dates", "start_date", "end_date"),
    )
    
    def __repr__(self) -> str:
        return f"<Project(id={self.id}, name='{self.name}', status='{self.status}')>"


class Location(Base):
    """Location ORM model
    
    Represents a physical location associated with a project.
    Includes address and geographic coordinates (latitude/longitude).
    """
    
    __tablename__ = "locations"
    
    # Primary key
    id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False,
    )
    
    # Foreign key with CASCADE delete
    project_id: Mapped[UUID] = mapped_column(
        PostgreSQLUUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,  # idx_locations_project_id
    )
    
    # Core fields
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    
    address: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    
    latitude: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(10, 8),
        nullable=True,
    )
    
    longitude: Mapped[Optional[Decimal]] = mapped_column(
        DECIMAL(11, 8),
        nullable=True,
    )
    
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    # Relationships
    project: Mapped["Project"] = relationship(
        "Project",
        back_populates="locations",
    )
    
    def __repr__(self) -> str:
        return f"<Location(id={self.id}, name='{self.name}', project_id={self.project_id})>"
