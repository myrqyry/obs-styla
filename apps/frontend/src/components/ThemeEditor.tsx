import React from 'react';

// TODO: Import shadcn/ui color picker and other controls when integrating
// import { ColorPicker } from 'shadcn/ui';

export interface ThemeVars {
  [key: string]: string;
}

export interface ThemeEditorProps {
  vars: ThemeVars;
  onChange: (vars: ThemeVars) => void;
}

/**
 * ThemeEditor: Exposes all palette and semantic color options for editing.
 * Uses compact, density-aware layout (M3 via Tailwind).
 */
export const ThemeEditor: React.FC<ThemeEditorProps> = ({ vars, onChange }) => {
  // Handler for color change
  const handleColorChange = (key: string, value: string) => {
    onChange({ ...vars, [key]: value });
  };

  return (
    <div className="grid grid-cols-1 gap-2 p-3 bg-surface-1 rounded-lg shadow-md">
      {Object.entries(vars).map(([key, value]) => (
        <div key={key} className="flex items-center gap-3">
          <label className="w-40 font-medium text-sm text-on-surface-variant" htmlFor={key}>
            {key}
          </label>
          {/* Replace with shadcn/ui ColorPicker when available */}
          <input
            id={key}
            type="color"
            value={value}
            className="w-8 h-8 border rounded"
            onChange={e => handleColorChange(key, e.target.value)}
          />
          <span className="ml-2 text-xs text-on-surface-variant">{value}</span>
        </div>
      ))}
    </div>
  );
};
