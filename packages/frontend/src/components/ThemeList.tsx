import React from 'react';
import { Theme } from '../types/theme';
import { ThemeItem } from './ThemeItem';

interface ThemeListProps {
  themes: Theme[];
  onDelete: (name: string) => Promise<void>;
  onDuplicate: (name: string) => Promise<void>;
  onEdit: (name: string) => Promise<void>;
}

export const ThemeList: React.FC<ThemeListProps> = ({
  themes,
  onDelete,
  onDuplicate,
  onEdit
}) => {
  if (themes.length === 0) {
    return (
      <div className="empty-state">
        <p>No themes generated yet. Click "Run Generation" to create some!</p>
      </div>
    );
  }

  return (
    <div className="theme-list">
      <h3>Generated Themes ({themes.length})</h3>
      <ul className="theme-items">
        {themes.map((theme) => (
          <ThemeItem
            key={theme.name}
            theme={theme}
            onDelete={onDelete}
            onDuplicate={onDuplicate}
            onEdit={onEdit}
          />
        ))}
      </ul>
    </div>
  );
};
