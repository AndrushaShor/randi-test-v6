/**
 * Project Form page - Create or edit a project
 */

import { useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { Button, Card, Input, Select, Textarea, LoadingSpinner } from '../components';
import { useProject, useCreateProject, useUpdateProject } from '../hooks';
import type { CreateProjectInput, ProjectStatus } from '../types';

export const ProjectForm = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const isEditing = !!id;

  const { data: project, isLoading: isLoadingProject } = useProject(Number(id));
  const createMutation = useCreateProject();
  const updateMutation = useUpdateProject();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CreateProjectInput>({
    defaultValues: {
      status: 'planning',
    },
  });

  // Populate form when editing
  useEffect(() => {
    if (project) {
      reset({
        name: project.name,
        description: project.description || '',
        status: project.status,
        start_date: project.start_date.split('T')[0],
        end_date: project.end_date ? project.end_date.split('T')[0] : '',
        budget: project.budget,
        client_name: project.client_name || '',
        project_manager: project.project_manager || '',
      });
    }
  }, [project, reset]);

  const onSubmit = async (data: CreateProjectInput) => {
    try {
      if (isEditing) {
        await updateMutation.mutateAsync({ id: Number(id), data });
      } else {
        await createMutation.mutateAsync(data);
      }
      navigate('/projects');
    } catch (error) {
      console.error('Error saving project:', error);
    }
  };

  if (isEditing && isLoadingProject) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  return (
    <div className="max-w-3xl">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">
          {isEditing ? 'Edit Project' : 'Create New Project'}
        </h1>
        <p className="mt-2 text-sm text-gray-600">
          {isEditing ? 'Update project information' : 'Add a new construction project'}
        </p>
      </div>

      <Card>
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Project Name */}
          <Input
            label="Project Name"
            required
            error={errors.name?.message}
            {...register('name', { required: 'Project name is required' })}
          />

          {/* Description */}
          <Textarea
            label="Description"
            rows={4}
            error={errors.description?.message}
            {...register('description')}
          />

          {/* Status */}
          <Select
            label="Status"
            required
            error={errors.status?.message}
            {...register('status', { required: 'Status is required' })}
          >
            <option value="planning">Planning</option>
            <option value="in-progress">In Progress</option>
            <option value="on-hold">On Hold</option>
            <option value="completed">Completed</option>
            <option value="cancelled">Cancelled</option>
          </Select>

          {/* Dates */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <Input
              type="date"
              label="Start Date"
              required
              error={errors.start_date?.message}
              {...register('start_date', { required: 'Start date is required' })}
            />
            <Input
              type="date"
              label="End Date"
              error={errors.end_date?.message}
              {...register('end_date')}
            />
          </div>

          {/* Budget */}
          <Input
            type="number"
            label="Budget"
            step="0.01"
            min="0"
            placeholder="0.00"
            error={errors.budget?.message}
            {...register('budget', {
              valueAsNumber: true,
              min: { value: 0, message: 'Budget must be positive' },
            })}
          />

          {/* Client & Manager */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <Input
              label="Client Name"
              error={errors.client_name?.message}
              {...register('client_name')}
            />
            <Input
              label="Project Manager"
              error={errors.project_manager?.message}
              {...register('project_manager')}
            />
          </div>

          {/* Form Actions */}
          <div className="flex justify-end gap-3">
            <Button
              type="button"
              variant="secondary"
              onClick={() => navigate('/projects')}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              isLoading={createMutation.isPending || updateMutation.isPending}
            >
              {isEditing ? 'Update Project' : 'Create Project'}
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
};
