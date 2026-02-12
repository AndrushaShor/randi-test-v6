/**
 * React Query hooks for locations
 */

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { locationsApi } from '../api';
import type { CreateLocationInput, UpdateLocationInput } from '../types';

export const useProjectLocations = (projectId: number) => {
  return useQuery({
    queryKey: ['locations', 'project', projectId],
    queryFn: () => locationsApi.getProjectLocations(projectId),
    enabled: projectId > 0,
  });
};

export const useLocation = (id: number) => {
  return useQuery({
    queryKey: ['locations', id],
    queryFn: () => locationsApi.getLocation(id),
    enabled: id > 0,
  });
};

export const useCreateLocation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateLocationInput) => locationsApi.createLocation(data),
    onSuccess: (_, variables) => {
      // Invalidate locations list for the project
      queryClient.invalidateQueries({
        queryKey: ['locations', 'project', variables.project_id],
      });
    },
  });
};

export const useUpdateLocation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: number; data: UpdateLocationInput }) =>
      locationsApi.updateLocation(id, data),
    onSuccess: (location) => {
      // Invalidate both the specific location and the project's locations list
      queryClient.invalidateQueries({ queryKey: ['locations', location.id] });
      if (location.project_id) {
        queryClient.invalidateQueries({
          queryKey: ['locations', 'project', location.project_id],
        });
      }
    },
  });
};

export const useDeleteLocation = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: number) => locationsApi.deleteLocation(id),
    onSuccess: () => {
      // Invalidate all location queries
      queryClient.invalidateQueries({ queryKey: ['locations'] });
    },
  });
};
