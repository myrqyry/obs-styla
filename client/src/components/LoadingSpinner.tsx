import React from 'react';
import './LoadingSpinner.css';

interface LoadingSpinnerProps {
  size?: 'small' | 'medium' | 'large';
  message?: string;
  overlay?: boolean;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
   size = 'medium',
   message,
  overlay = false
 }) => {
  const spinner = (
    <div className={`spinner-container spinner-${size}`}>
      <div className="spinner" role="status" aria-label="Loading">
        <div className="spinner-circle"></div>
      </div>
      {message && <p className="spinner-message">{message}</p>}
    </div>
  );

   if (overlay) {
    return (
      <div className="spinner-overlay">
        {spinner}
      </div>
    );
  }

   return spinner;
};
