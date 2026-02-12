/**
 * LocationList component - Display list of locations for a project
 * This is a placeholder for implementation
 */

import { Link } from 'react-router-dom';
import { Card, Button, LoadingSpinner } from '../../components';
import { useProjectLocations, useDeleteLocation } from '../../hooks';

interface LocationListProps {
  projectId: number;
}

export const LocationList = ({ projectId }: LocationListProps) => {
  const { data, isLoading, error } = useProjectLocations(projectId);
  const deleteMutation = useDeleteLocation();

  const handleDelete = async (locationId: number) => {
    if (window.confirm('Are you sure you want to delete this location?')) {
      try {
        await deleteMutation.mutateAsync(locationId);
      } catch (error) {
        console.error('Error deleting location:', error);
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-8">
        <LoadingSpinner />
      </div>
    );
  }

  if (error) {
    return (
      <Card>
        <p className="text-red-600 text-center py-4">Error loading locations</p>
      </Card>
    );
  }

  const locations = data?.locations || [];

  if (locations.length === 0) {
    return (
      <Card>
        <div className="text-center py-8">
          <p className="text-gray-500 mb-4">No locations added yet</p>
          <Link to={`/projects/${projectId}/locations/new`}>
            <Button>Add First Location</Button>
          </Link>
        </div>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      {locations.map((location) => (
        <Card key={location.id}>
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h3 className="text-lg font-medium text-gray-900">{location.name}</h3>
              <p className="mt-1 text-sm text-gray-600">{location.address}</p>
              {(location.city || location.state || location.zip_code) && (
                <p className="text-sm text-gray-600">
                  {[location.city, location.state, location.zip_code]
                    .filter(Boolean)
                    .join(', ')}
                </p>
              )}
              {location.notes && (
                <p className="mt-2 text-sm text-gray-500">{location.notes}</p>
              )}
            </div>
            <div className="flex gap-2 ml-4">
              <Link to={`/projects/${projectId}/locations/${location.id}/edit`}>
                <Button variant="secondary" size="sm">
                  Edit
                </Button>
              </Link>
              <Button
                variant="danger"
                size="sm"
                onClick={() => handleDelete(location.id)}
                isLoading={deleteMutation.isPending}
              >
                Delete
              </Button>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
};
