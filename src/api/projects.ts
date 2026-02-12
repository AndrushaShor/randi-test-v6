/**
 * Projects API service
 * Handles all project-related API calls
 */

import { apiClient } from './client';
import type {
  Project,
  ProjectsResponse,
  CreateProjectInput,
  UpdateProjectInput,
  ProjectFilters,
} from '../types';

export const projectsApi = {
  /**
   * Get all projects with optional filters
   */
  getProjects: async (filters?: ProjectFilters): Promise<ProjectsResponse> => {
    const params = new URLSearchParams();
    if (filters?.status) params.append('status', filters.status);
    if (filters?.search) params.append('search', filters.search);
    if (filters?.start_date_from) params.append('start_date_from', filters.start_date_from);
    if (filters?.start_date_to) params.append('start_date_to', filters.start_date_to);
    
    const response = await apiClient.get<ProjectsResponse>(`/projects?${params.toString()}`);
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
