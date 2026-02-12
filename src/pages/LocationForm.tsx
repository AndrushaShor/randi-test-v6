/**
 * Location Form page - Create or edit a location
 */

import { useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { Button, Card, Input, Textarea, LoadingSpinner } from '../components';
import { useLocation, useCreateLocation, useUpdateLocation } from '../hooks';
import type { CreateLocationInput } from '../types';

export const LocationForm = () => {
  const { projectId, locationId } = useParams<{ projectId: string; locationId: string }>();
  const navigate = useNavigate();
  const isEditing = !!locationId;

  const { data: location, isLoading: isLoadingLocation } = useLocation(Number(locationId));
  const createMutation = useCreateLocation();
  const updateMutation = useUpdateLocation();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CreateLocationInput>({
    defaultValues: {
      project_id: Number(projectId),
    },
  });

  // Populate form when editing
  useEffect(() => {
    if (location) {
      reset({
        project_id: location.project_id,
        name: location.name,
        address: location.address,
        city: location.city || '',
        state: location.state || '',
        zip_code: location.zip_code || '',
        country: location.country || '',
        latitude: location.latitude,
        longitude: location.longitude,
        notes: location.notes || '',
      });
    }
  }, [location, reset]);

  const onSubmit = async (data: CreateLocationInput) => {
    try {
      if (isEditing) {
        await updateMutation.mutateAsync({ id: Number(locationId), data });
      } else {
        await createMutation.mutateAsync(data);
      }
      navigate(`/projects/${projectId}`);
    } catch (error) {
      console.error('Error saving location:', error);
    }
  };

  if (isEditing && isLoadingLocation) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="max-w-3xl">
      <div className="mb-6">
        <Button variant="ghost" onClick={() => navigate(`/projects/${projectId}`)}>
          <svg
            className="h-5 w-5"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z"
              clipRule="evenodd"
            />
          </svg>
          Back to Project
        </Button>
        <h1 className="mt-4 text-3xl font-bold text-gray-900">
          {isEditing ? 'Edit Location' : 'Add New Location'}
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          {isEditing ? 'Update location information' : 'Add a new location to this project'}
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Location Name */}
          <Input
            label="Location Name"
            required
            error={errors.name?.message}
            {...register('name', { required: 'Location name is required' })}
          />

          {/* Address */}
          <Input
            label="Address"
            required
            error={errors.address?.message}
            {...register('address', { required: 'Address is required' })}
          />

          {/* City, State, ZIP */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
            <Input
              label="City"
              error={errors.city?.message}
              {...register('city')}
            />
            <Input
              label="State"
              error={errors.state?.message}
              {...register('state')}
            />
            <Input
              label="ZIP Code"
              error={errors.zip_code?.message}
              {...register('zip_code')}
            />
          </div>

          {/* Country */}
          <Input
            label="Country"
            error={errors.country?.message}
            {...register('country')}
          />

          {/* Coordinates */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <Input
              type="number"
              step="any"
              label="Latitude"
              placeholder="e.g. 40.7128"
              error={errors.latitude?.message}
              {...register('latitude', { valueAsNumber: true })}
            />
            <Input
              type="number"
              step="any"
              label="Longitude"
              placeholder="e.g. -74.0060"
              error={errors.longitude?.message}
              {...register('longitude', { valueAsNumber: true })}
            />
          </div>

          {/* Notes */}
          <Textarea
            label="Notes"
            rows={4}
            placeholder="Additional information about this location"
            error={errors.notes?.message}
            {...register('notes')}
          />

          {/* Form Actions */}
          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate(`/projects/${projectId}`)}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={createMutation.isPending || updateMutation.isPending}
            >
              {isEditing ? 'Update Location' : 'Add Location'}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
