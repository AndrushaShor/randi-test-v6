/**
 * ProjectCard component - Reusable card for displaying project summary
 * This is a placeholder for the style specialist to implement
 */

import { Card, Badge } from '../../components';
import { formatDate, formatCurrency } from '../../utils';
import type { Project } from '../../types';

interface ProjectCardProps {
  project: Project;
  onClick?: () => void;
}

export const ProjectCard = ({ project, onClick }: ProjectCardProps) => {
  return (
    <Card hoverable onClick={onClick}>
      <div className="space-y-3">
        <div className="flex items-start justify-between">
          <h3 className="text-lg font-semibold text-gray-900">{project.name}</h3>
          <Badge variant={project.status}>{project.status.replace('-', ' ')}</Badge>
        </div>
        
        {project.description && (
          <p className="text-sm text-gray-600 line-clamp-2">{project.description}</p>
        )}
        
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-gray-500">Start:</span>
            <span className="ml-1 text-gray-900">{formatDate(project.start_date)}</span>
          </div>
          {project.budget && (
            <div>
              <span className="text-gray-500">Budget:</span>
              <span className="ml-1 text-gray-900">{formatCurrency(project.budget)}</span>
            </div>
          )}
        </div>
      </div>
    </Card>
  );
};
