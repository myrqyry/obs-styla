import React, { useContext, useState } from 'react';
import { ThemeContext } from '../../context/ThemeContext';

interface ScenesPanelProps {
  currentScene: string;
  onSceneChange: (scene: string) => void;
}

const ScenesPanel: React.FC<ScenesPanelProps> = ({ currentScene, onSceneChange }) => {
  const { state } = useContext(ThemeContext);
  const { colors } = state;

  const scenes = [
    'Main Scene',
    'Starting Soon',
    'Be Right Back',
    'Ending Soon',
    'Gameplay',
    'Interview',
    'Outro'
  ];

  const SceneItem = ({ scene, isActive }: { scene: string; isActive: boolean }) => (
    <button
      className={`w-full text-left px-3 py-2 rounded transition-all duration-200 ${
        isActive
          ? 'shadow-lg transform scale-105'
          : 'hover:shadow-md hover:transform hover:scale-102'
      }`}
      style={{
        backgroundColor: isActive ? colors.accent : colors.button_background,
        color: isActive ? colors.accent_text : colors.button_text,
        border: `1px solid ${isActive ? colors.accent : colors.ui_border}`
      }}
      onClick={() => onSceneChange(scene)}
    >
      <div className="flex items-center justify-between">
        <span className="font-medium">{scene}</span>
        {isActive && <span className="text-xs opacity-75">●</span>}
      </div>
    </button>
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
        Scenes
      </div>
      <div className="flex-1 p-3 overflow-y-auto">
        <div className="space-y-2">
          {scenes.map((scene) => (
            <SceneItem
              key={scene}
              scene={scene}
              isActive={scene === currentScene}
            />
          ))}
        </div>

        {/* Add scene button */}
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
              <span>Add Scene</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ScenesPanel;
