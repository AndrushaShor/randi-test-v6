/**
 * Core type definitions for the Construction Project Portal
 * Aligned with Backend API contract from .hive/messages/api/api-contract.json
 */

// Match exact status values from API contract
export type ProjectStatus = 'active' | 'completed' | 'on-hold';

// Coordinates type matching API contract
export interface Coordinates {
  lat: number;  // -90 to 90
  lng: number;  // -180 to 180
}

// Project types matching API contract
export interface Project {
  id: number;
  name: string;
  description?: string | null;
  status: ProjectStatus;
  start_date: string; // YYYY-MM-DD format
  end_date?: string | null; // YYYY-MM-DD format
  budget?: number | null;
  created_at: string; // ISO 8601 datetime
  updated_at: string; // ISO 8601 datetime
}

export interface Location {
  id: number;
  project_id: number;
  name: string;
  address: string;
  coordinates?: Coordinates | null;
  notes?: string | null;
  created_at: string; // ISO 8601 datetime
  updated_at: string; // ISO 8601 datetime
}

// Form input types matching API contract schemas
export interface CreateProjectInput {
  name: string; // 1-200 chars
  description?: string | null; // max 2000 chars
  status?: ProjectStatus; // defaults to 'active'
  start_date: string; // YYYY-MM-DD
  end_date?: string | null; // YYYY-MM-DD
  budget?: number | null; // min 0
}

export interface UpdateProjectInput {
  name?: string; // 1-200 chars
  description?: string | null;
  status?: ProjectStatus;
  start_date?: string; // YYYY-MM-DD
  end_date?: string | null;
  budget?: number | null;
}

export interface CreateLocationInput {
  name: string; // 1-200 chars
  address: string; // 1-500 chars
  coordinates?: Coordinates | null;
  notes?: string | null; // max 2000 chars
}

export interface UpdateLocationInput {
  name?: string;
  address?: string;
  coordinates?: Coordinates | null;
  notes?: string | null;
}

// API Response types matching OpenAPI spec
export interface ProjectListResponse {
  items: Project[];
  total: number;
  limit: number;
  offset: number;
}

export interface LocationListResponse {
  items: Location[];
  total: number;
}

// Query parameter types for filtering
export interface ProjectFilters {
  status?: ProjectStatus;
  name?: string; // search by name
  start_date_from?: string; // YYYY-MM-DD
  start_date_to?: string; // YYYY-MM-DD
  limit?: number; // 1-100, default 20
  offset?: number; // default 0
}

// Dashboard metrics type (computed from projects)
export interface ProjectMetrics {
  total_projects: number;
  active_projects: number;
  completed_projects: number;
  on_hold_projects: number;
  total_budget: number;
}

// Error response type
export interface APIError {
  detail: string | Array<{
    loc: string[];
    msg: string;
    type: string;
  }>;
}
