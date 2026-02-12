/**
 * Locations API service
 * Handles all location-related API calls
 */

import { apiClient } from './client';
import type {
  Location,
  CreateLocationInput,
  UpdateLocationInput,
} from '../types';

export const locationsApi = {
  /**
   * Get all locations for a project
   * Returns array of locations (not paginated according to API contract)
   */
  getProjectLocations: async (projectId: number): Promise<Location[]> => {
    const response = await apiClient.get<Location[]>(`/projects/${projectId}/locations`);
    return response.data;
  },

  /**
   * Create a new location for a project
   */
  createLocation: async (projectId: number, data: CreateLocationInput): Promise<Location> => {
    const response = await apiClient.post<Location>(
      `/projects/${projectId}/locations`,
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
