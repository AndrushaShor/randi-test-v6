/**
 * Projects API service
 * Handles all project-related API calls
 */

import { apiClient } from './client';
import type {
  Project,
  ProjectListResponse,
  CreateProjectInput,
  UpdateProjectInput,
  ProjectFilters,
} from '../types';

export const projectsApi = {
  /**
   * Get all projects with optional filters
   * Returns paginated response with items, total, limit, offset
   */
  getProjects: async (filters?: ProjectFilters): Promise<ProjectListResponse> => {
    const params = new URLSearchParams();
    if (filters?.status) params.append('status', filters.status);
    if (filters?.name) params.append('name', filters.name);
    if (filters?.start_date_from) params.append('start_date_from', filters.start_date_from);
    if (filters?.start_date_to) params.append('start_date_to', filters.start_date_to);
    if (filters?.limit) params.append('limit', filters.limit.toString());
    if (filters?.offset) params.append('offset', filters.offset.toString());
    
    const response = await apiClient.get<ProjectListResponse>(`/projects?${params.toString()}`);
    return response.data;
  },

  /**
   * Get a single project by ID
   */
  getProject: async (id: number): Promise<Project> => {
    const response = await apiClient.get<Project>(`/projects/${id}`);
    return response.data;
  },

  /**
   * Create a new project
   */
  createProject: async (data: CreateProjectInput): Promise<Project> => {
    const response = await apiClient.post<Project>('/projects', data);
    return response.data;
  },

  /**
   * Update an existing project
   */
  updateProject: async (id: number, data: UpdateProjectInput): Promise<Project> => {
    const response = await apiClient.put<Project>(`/projects/${id}`, data);
    return response.data;
  },

  /**
   * Delete a project
   */
  deleteProject: async (id: number): Promise<void> => {
    await apiClient.delete(`/projects/${id}`);
  },
};
