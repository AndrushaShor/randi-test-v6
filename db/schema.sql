-- Database Schema for Projects and Locations
-- Design: 1:N relationship (one Project has many Locations)

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Projects Table
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    start_date DATE NOT NULL,
    end_date DATE,
    budget DECIMAL(15, 2),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Locations Table
CREATE TABLE locations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    address VARCHAR(500),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_locations_project
        FOREIGN KEY (project_id)
        REFERENCES projects(id)
        ON DELETE CASCADE
);

-- Performance Indexes
-- Index on project name for search operations
CREATE INDEX idx_projects_name ON projects(name);

-- Index on project status for filtering operations
CREATE INDEX idx_projects_status ON projects(status);

-- Index on locations project_id for foreign key lookups and joins
CREATE INDEX idx_locations_project_id ON locations(project_id);

-- Optional: Composite index for date range queries
CREATE INDEX idx_projects_dates ON projects(start_date, end_date);

-- Optional: GIS index for location coordinates (if using PostGIS in future)
-- CREATE INDEX idx_locations_coordinates ON locations(latitude, longitude);

-- Comments for documentation
COMMENT ON TABLE projects IS 'Main projects table with project metadata';
COMMENT ON TABLE locations IS 'Project locations with geographic information';
COMMENT ON COLUMN projects.status IS 'Project status (e.g., planning, active, completed, archived)';
COMMENT ON COLUMN projects.budget IS 'Project budget in currency units';
COMMENT ON COLUMN locations.latitude IS 'Latitude coordinate (WGS84)';
COMMENT ON COLUMN locations.longitude IS 'Longitude coordinate (WGS84)';
