/**
 * Locations API service
 * Handles all location-related API calls
 */

import { apiClient } from './client';
import type {
  Location,
  LocationsResponse,
  CreateLocationInput,
  UpdateLocationInput,
} from '../types';

export const locationsApi = {
  /**
   * Get all locations for a project
   */
  getProjectLocations: async (projectId: number): Promise<LocationsResponse> => {
    const response = await apiClient.get<LocationsResponse>(`/projects/${projectId}/locations`);
    return response.data;
  },

  /**
   * Get a single location by ID
   */
  getLocation: async (id: number): Promise<Location> => {
    const response = await apiClient.get<Location>(`/locations/${id}`);
    return response.data;
  },

  /**
   * Create a new location for a project
   */
  createLocation: async (data: CreateLocationInput): Promise<Location> => {
    const response = await apiClient.post<Location>(
      `/projects/${data.project_id}/locations`,
      data
    );
    return response.data;
  },

  /**
   * Update an existing location
   */
  updateLocation: async (id: number, data: UpdateLocationInput): Promise<Location> => {
    const response = await apiClient.put<Location>(`/locations/${id}`, data);
    return response.data;
  },

  /**
   * Delete a location
   */
  deleteLocation: async (id: number): Promise<void> => {
    await apiClient.delete(`/locations/${id}`);
  },
};
