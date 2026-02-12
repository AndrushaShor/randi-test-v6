/**
 * Badge component for status indicators
 */

import { ReactNode } from 'react';
import type { ProjectStatus } from '../types';

interface BadgeProps {
  children: ReactNode;
  variant?: ProjectStatus | 'default';
  size?: 'sm' | 'md';
}

export const Badge = ({ children, variant = 'default', size = 'md' }: BadgeProps) => {
  const sizeStyles = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-3 py-1 text-sm',
  };

  const variantStyles = {
    planning: 'bg-blue-100 text-blue-800',
    'in-progress': 'bg-green-100 text-green-800',
    'on-hold': 'bg-yellow-100 text-yellow-800',
    completed: 'bg-gray-100 text-gray-800',
    cancelled: 'bg-red-100 text-red-800',
    default: 'bg-gray-100 text-gray-800',
  };

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full ${sizeStyles[size]} ${variantStyles[variant]}`}
    >
      {children}
    </span>
  );
};
