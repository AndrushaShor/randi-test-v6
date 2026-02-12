/**
 * Form validation utility functions
 */

/**
 * Validate required field
 */
export const validateRequired = (value: string | undefined): string | undefined => {
  if (!value || value.trim() === '') {
    return 'This field is required';
  }
  return undefined;
};

/**
 * Validate date format
 */
export const validateDate = (value: string | undefined): string | undefined => {
  if (!value) return undefined;
  
  const date = new Date(value);
  if (isNaN(date.getTime())) {
    return 'Invalid date format';
  }
  return undefined;
};

/**
 * Validate end date is after start date
 */
export const validateEndDate = (endDate: string | undefined, startDate: string): string | undefined => {
  if (!endDate || !startDate) return undefined;
  
  const start = new Date(startDate);
  const end = new Date(endDate);
  
  if (end <= start) {
    return 'End date must be after start date';
  }
  return undefined;
};

/**
 * Validate positive number
 */
export const validatePositiveNumber = (value: number | undefined): string | undefined => {
  if (value !== undefined && value < 0) {
    return 'Value must be positive';
  }
  return undefined;
};

/**
 * Validate email format
 */
export const validateEmail = (value: string | undefined): string | undefined => {
  if (!value) return undefined;
  
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRegex.test(value)) {
    return 'Invalid email format';
  }
  return undefined;
};
