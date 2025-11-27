import React, { useContext, useState } from 'react';
import { ThemeContext } from '../../context/ThemeContext';

interface Source {
  id: string;
  name: string;
  type: string;
  icon: string;
  visible: boolean;
}

interface SourcesPanelProps {
  sources: Source[];
  onSourceToggle: (sourceId: string) => void;
}

const SourcesPanel: React.FC<SourcesPanelProps> = ({ sources, onSourceToggle }) => {
  const { state } = useContext(ThemeContext);
  const { colors } = state;

  const SourceItem = ({ source }: { source: Source }) => (
    <div
      className="flex items-center justify-between px-3 py-2 rounded transition-all duration-200 hover:shadow-md"
      style={{
        backgroundColor: colors.button_background,
        border: `1px solid ${colors.ui_border}`
      }}
    >
      <div className="flex items-center space-x-3">
        <button
          className={`w-4 h-4 rounded transition-colors ${
            source.visible ? 'opacity-100' : 'opacity-50'
          }`}
          style={{
            backgroundColor: source.visible ? colors.success : colors.ui_border
          }}
          onClick={() => onSourceToggle(source.id)}
          title={source.visible ? 'Hide source' : 'Show source'}
        >
          👁️
        </button>
        <span className="text-sm">{source.icon}</span>
        <span
          className="font-medium text-sm"
          style={{ color: colors.button_text }}
        >
          {source.name}
        </span>
      </div>
      <span
        className="text-xs px-2 py-1 rounded"
        style={{
          backgroundColor: colors.ui_background_alt,
          color: colors.ui_text_dark
        }}
      >
        {source.type}
      </span>
    </div>
  );

  return (
    <div className="flex flex-col h-full">
      <div
        className="font-bold py-2 px-3 border-b text-center text-sm"
        style={{
          backgroundColor: colors.dock_background,
          borderColor: colors.ui_border,
          color: colors.ui_text
        }}
      >
        Sources
      </div>
      <div className="flex-1 p-3 overflow-y-auto">
        <div className="space-y-2">
          {sources.map((source) => (
            <SourceItem key={source.id} source={source} />
          ))}
        </div>

        {/* Add source button */}
        <div className="mt-4 pt-3 border-t" style={{ borderColor: colors.ui_border }}>
          <button
            className="w-full px-3 py-2 rounded text-sm transition-colors"
            style={{
              backgroundColor: colors.button_background,
              color: colors.button_text,
              border: `1px solid ${colors.ui_border}`
            }}
          >
            <div className="flex items-center justify-center space-x-2">
              <span>+</span>
              <span>Add Source</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default SourcesPanel;
