"""create_projects_and_locations_tables

Revision ID: 2d4ebf6ab1f7
Revises: 
Create Date: 2026-02-12 15:08:49.685818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '2d4ebf6ab1f7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Create projects and locations tables."""
    # Create projects table
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=True),
        sa.Column('budget', sa.DECIMAL(precision=15, scale=2), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_projects')
    )
    
    # Create indexes on projects table
    op.create_index('ix_projects_name', 'projects', ['name'], unique=False)
    op.create_index('ix_projects_status', 'projects', ['status'], unique=False)
    op.create_index('idx_projects_dates', 'projects', ['start_date', 'end_date'], unique=False)
    
    # Create locations table
    op.create_table(
        'locations',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('address', sa.String(length=500), nullable=True),
        sa.Column('latitude', sa.DECIMAL(precision=10, scale=8), nullable=True),
        sa.Column('longitude', sa.DECIMAL(precision=11, scale=8), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id', name='pk_locations'),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name='fk_locations_project_id', ondelete='CASCADE')
    )
    
    # Create index on locations table
    op.create_index('ix_locations_project_id', 'locations', ['project_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema: Drop locations and projects tables."""
    # Drop locations table first (has foreign key to projects)
    op.drop_index('ix_locations_project_id', table_name='locations')
    op.drop_table('locations')
    
    # Drop projects table
    op.drop_index('idx_projects_dates', table_name='projects')
    op.drop_index('ix_projects_status', table_name='projects')
    op.drop_index('ix_projects_name', table_name='projects')
    op.drop_table('projects')
