/**
 * Core type definitions for the Construction Project Portal
 * Based on expected API contract from Backend team
 */

export type ProjectStatus = 'planning' | 'in-progress' | 'on-hold' | 'completed' | 'cancelled';

export interface Project {
  id: number;
  name: string;
  description?: string;
  status: ProjectStatus;
  start_date: string; // ISO 8601 date string
  end_date?: string; // ISO 8601 date string
  budget?: number;
  actual_cost?: number;
  client_name?: string;
  project_manager?: string;
  created_at: string;
  updated_at: string;
}

export interface Location {
  id: number;
  project_id: number;
  name: string;
  address: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  latitude?: number;
  longitude?: number;
  notes?: string;
  created_at: string;
  updated_at: string;
}

// Form input types (for create/update operations)
export interface CreateProjectInput {
  name: string;
  description?: string;
  status: ProjectStatus;
  start_date: string;
  end_date?: string;
  budget?: number;
  client_name?: string;
  project_manager?: string;
}

export interface UpdateProjectInput extends Partial<CreateProjectInput> {
  id: number;
}

export interface CreateLocationInput {
  project_id: number;
  name: string;
  address: string;
  city?: string;
  state?: string;
  zip_code?: string;
  country?: string;
  latitude?: number;
  longitude?: number;
  notes?: string;
}

export interface UpdateLocationInput extends Partial<CreateLocationInput> {
  id: number;
}

// API Response types
export interface ProjectsResponse {
  projects: Project[];
  total: number;
}

export interface LocationsResponse {
  locations: Location[];
  total: number;
}

// Query parameter types for filtering
export interface ProjectFilters {
  status?: ProjectStatus;
  search?: string;
  start_date_from?: string;
  start_date_to?: string;
  end_date_from?: string;
  end_date_to?: string;
}

// Dashboard metrics type
export interface ProjectMetrics {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  total_budget: number;
  total_actual_cost: number;
}
