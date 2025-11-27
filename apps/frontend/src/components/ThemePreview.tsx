import React from 'react';

export interface ThemePreviewProps {
  vars: Record<string, string>;
}

/**
 * ThemePreview: Renders a live preview of the theme using the current color variables.
 * Applies the colors as inline CSS variables for demonstration.
 */
export const ThemePreview: React.FC<ThemePreviewProps> = ({ vars }) => {
  // Build CSS variable style object
  const style: React.CSSProperties = Object.fromEntries(
    Object.entries(vars).map(([k, v]) => [`--${k}`, v])
  );

  return (
    <div
      className="w-full rounded-lg shadow p-6 flex flex-col gap-4 bg-surface-2 border border-outline-variant"
      style={style}
    >
      <h2 className="text-xl font-bold mb-2" style={{ color: 'var(--text-color, #222)' }}>
        Theme Preview
      </h2>
      <div className="flex gap-4 items-center">
        <div
          className="w-16 h-16 rounded-full border"
          style={{ background: 'var(--primary-color, #3b82f6)' }}
        />
        <div className="flex flex-col gap-1">
          <span className="font-medium" style={{ color: 'var(--primary-color, #3b82f6)' }}>
            Primary
          </span>
          <span className="text-xs" style={{ color: 'var(--text-color, #222)' }}>
            {vars['primary-color']}
          </span>
        </div>
      </div>
      <div className="flex gap-4 items-center">
        <div
          className="w-16 h-16 rounded-full border"
          style={{ background: 'var(--secondary-color, #8b5cf6)' }}
        />
        <div className="flex flex-col gap-1">
          <span className="font-medium" style={{ color: 'var(--secondary-color, #8b5cf6)' }}>
            Secondary
          </span>
          <span className="text-xs" style={{ color: 'var(--text-color, #222)' }}>
            {vars['secondary-color']}
          </span>
        </div>
      </div>
      <div className="flex flex-col gap-2 mt-4">
        <div
          className="rounded p-3"
          style={{ background: 'var(--background-color, #1f2937)', color: 'var(--text-color, #f3f4f6)' }}
        >
          <span className="font-semibold">Background Example</span>
        </div>
      </div>
    </div>
  );
};
