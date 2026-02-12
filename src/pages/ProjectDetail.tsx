/**
 * Project Detail page - View project details and manage locations
 */

import { useParams, useNavigate, Link } from 'react-router-dom';
import { Button, Card, LoadingSpinner, Badge } from '../components';
import { useProject, useDeleteProject } from '../hooks';
import { formatCurrency, formatDate } from '../utils';

export const ProjectDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: project, isLoading, error } = useProject(Number(id));
  const deleteMutation = useDeleteProject();

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await deleteMutation.mutateAsync(Number(id));
        navigate('/projects');
      } catch (error) {
        console.error('Error deleting project:', error);
      }
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error || !project) {
    return (
      <div className="text-center text-red-600">
        <p>Error loading project details</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-4">
          <Button variant="ghost" onClick={() => navigate('/projects')}>
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
            Back
          </Button>
          <div>
            <div className="flex items-center gap-3">
              <h1 className="text-3xl font-bold text-gray-900">{project.name}</h1>
              <Badge variant={project.status}>{project.status.replace('-', ' ')}</Badge>
            </div>
          </div>
        </div>
        <div className="flex gap-3">
          <Link to={`/projects/${id}/edit`}>
            <Button variant="secondary">Edit Project</Button>
          </Link>
          <Button
            variant="danger"
            onClick={handleDelete}
            isLoading={deleteMutation.isPending}
          >
            Delete
          </Button>
        </div>
      </div>

      {/* Project Information */}
      <Card>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Project Information</h2>
        <dl className="grid grid-cols-1 gap-x-4 gap-y-6 sm:grid-cols-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">Description</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {project.description || 'No description provided'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Client Name</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {project.client_name || 'N/A'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Project Manager</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {project.project_manager || 'N/A'}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Start Date</dt>
            <dd className="mt-1 text-sm text-gray-900">{formatDate(project.start_date)}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">End Date</dt>
            <dd className="mt-1 text-sm text-gray-900">{formatDate(project.end_date)}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Budget</dt>
            <dd className="mt-1 text-sm text-gray-900">{formatCurrency(project.budget)}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Actual Cost</dt>
            <dd className="mt-1 text-sm text-gray-900">
              {formatCurrency(project.actual_cost)}
            </dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Created</dt>
            <dd className="mt-1 text-sm text-gray-900">{formatDate(project.created_at)}</dd>
          </div>
        </dl>
      </Card>

      {/* Locations Section */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Locations</h2>
          <Link to={`/projects/${id}/locations/new`}>
            <Button>
              <svg
                className="-ml-1 mr-2 h-5 w-5"
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z"
                  clipRule="evenodd"
                />
              </svg>
              Add Location
            </Button>
          </Link>
        </div>
        <Card>
          <p className="text-gray-500 text-center py-8">
            Location list will be implemented next
          </p>
        </Card>
      </div>
    </div>
  );
};
