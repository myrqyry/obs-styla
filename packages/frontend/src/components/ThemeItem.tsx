import React from 'react';
import { Theme } from '../types/theme';

interface ThemeItemProps {
  theme: Theme;
  onDelete: (name: string) => Promise<void>;
  onDuplicate: (name: string) => Promise<void>;
  onEdit: (name: string) => Promise<void>;
}

export const ThemeItem: React.FC<ThemeItemProps> = ({ theme, onDelete, onDuplicate, onEdit }) => {
  return (
    <li>
      <a href={`/api/themes/${encodeURIComponent(theme.name)}`} target="_blank">{theme.name} ({theme.size} bytes)</a>
      <button onClick={() => onDelete(theme.name)}>Delete</button>
      <button onClick={() => onDuplicate(theme.name)}>Duplicate</button>
      <button onClick={() => onEdit(theme.name)}>Edit</button>
      <button onClick={() => window.open(`/api/themes/${encodeURIComponent(theme.name)}`, '_blank')}>Preview</button>
    </li>
  );
};
