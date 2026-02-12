/**
 * Reusable Card component
 */

import { ReactNode } from 'react';

interface CardProps {
  children: ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hoverable?: boolean;
}

export const Card = ({
  children,
  className = '',
  padding = 'md',
  hoverable = false,
}: CardProps) => {
  const paddingStyles = {
    none: '',
    sm: 'p-4',
    md: 'p-6',
    lg: 'p-8',
  };

  return (
    <div
      className={`bg-white rounded-lg shadow-sm border border-gray-200 ${
        paddingStyles[padding]
      } ${hoverable ? 'hover:shadow-md transition-shadow cursor-pointer' : ''} ${className}`}
    >
      {children}
    </div>
  );
};
