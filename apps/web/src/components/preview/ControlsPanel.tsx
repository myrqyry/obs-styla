import React, { useContext } from 'react';
import { ThemeContext } from '../../context/ThemeContext';

interface ControlsPanelProps {
  isRecording: boolean;
  isStreaming: boolean;
  isVirtualCam: boolean;
  studioMode: boolean;
  onRecordingChange: (recording: boolean) => void;
  onStreamingChange: (streaming: boolean) => void;
  onVirtualCamChange: (virtualCam: boolean) => void;
  onStudioModeChange: (studioMode: boolean) => void;
}

const ControlsPanel: React.FC<ControlsPanelProps> = ({
  isRecording,
  isStreaming,
  isVirtualCam,
  studioMode,
  onRecordingChange,
  onStreamingChange,
  onVirtualCamChange,
  onStudioModeChange,
}) => {
  const { state } = useContext(ThemeContext);
  const { colors } = state;

  const ControlButton = ({
    children,
    active,
    onClick,
    activeColor,
    disabled = false
  }: {
    children: React.ReactNode;
    active?: boolean;
    onClick?: () => void;
    activeColor?: string;
    disabled?: boolean;
  }) => (
    <button
      className={`flex-1 px-3 py-2 rounded font-medium text-sm transition-all duration-200 ${
        active
          ? 'shadow-lg transform scale-105'
          : 'hover:shadow-md hover:transform hover:scale-102'
      }`}
      style={{
        backgroundColor: active ? (activeColor || colors.accent) : colors.button_background,
        color: active ? colors.accent_text : colors.button_text,
        border: `1px solid ${active ? (activeColor || colors.accent) : colors.ui_border}`,
        opacity: disabled ? 0.5 : 1,
      }}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );

  return (
    <div className="flex flex-col h-1/2">
      <div
        className="font-bold py-2 px-3 border-b text-center text-sm"
        style={{
          backgroundColor: colors.dock_background,
          borderColor: colors.ui_border,
          color: colors.ui_text
        }}
      >
        Controls
      </div>
      <div className="flex-1 p-3 overflow-y-auto">
        <div className="space-y-3">
          {/* Main control buttons */}
          <div className="grid grid-cols-2 gap-2">
            <ControlButton
              active={isStreaming}
              onClick={() => onStreamingChange(!isStreaming)}
              activeColor={colors.success}
            >
              <div className="flex flex-col items-center space-y-1">
                <span className="text-lg">🎥</span>
                <span className="text-xs">Stream</span>
              </div>
            </ControlButton>

            <ControlButton
              active={isRecording}
              onClick={() => onRecordingChange(!isRecording)}
              activeColor={colors.error}
            >
              <div className="flex flex-col items-center space-y-1">
                <span className="text-lg">⏺️</span>
                <span className="text-xs">Record</span>
              </div>
            </ControlButton>

            <ControlButton
              active={isVirtualCam}
              onClick={() => onVirtualCamChange(!isVirtualCam)}
              activeColor={colors.info}
            >
              <div className="flex flex-col items-center space-y-1">
                <span className="text-lg">📹</span>
                <span className="text-xs">VCam</span>
              </div>
            </ControlButton>

            <ControlButton
              active={studioMode}
              onClick={() => onStudioModeChange(!studioMode)}
            >
              <div className="flex flex-col items-center space-y-1">
                <span className="text-lg">🎭</span>
                <span className="text-xs">Studio</span>
              </div>
            </ControlButton>
          </div>

          {/* Secondary controls */}
          <div className="space-y-2">
            <button
              className="w-full px-3 py-2 rounded text-sm transition-colors"
              style={{
                backgroundColor: colors.button_background,
                color: colors.button_text,
                border: `1px solid ${colors.ui_border}`
              }}
            >
              <div className="flex items-center justify-between">
                <span>Settings</span>
                <span>⚙️</span>
              </div>
            </button>

            <button
              className="w-full px-3 py-2 rounded text-sm transition-colors"
              style={{
                backgroundColor: colors.button_background,
                color: colors.button_text,
                border: `1px solid ${colors.ui_border}`
              }}
            >
              <div className="flex items-center justify-between">
                <span>Scene Transitions</span>
                <span>🔄</span>
              </div>
            </button>

            <button
              className="w-full px-3 py-2 rounded text-sm transition-colors"
              style={{
                backgroundColor: colors.button_background,
                color: colors.button_text,
                border: `1px solid ${colors.ui_border}`
              }}
            >
              <div className="flex items-center justify-between">
                <span>Filters</span>
                <span>🎨</span>
              </div>
            </button>

            <button
              className="w-full px-3 py-2 rounded text-sm transition-colors"
              style={{
                backgroundColor: colors.button_background,
                color: colors.button_text,
                border: `1px solid ${colors.ui_border}`
              }}
            >
              <div className="flex items-center justify-between">
                <span>Sources</span>
                <span>📦</span>
              </div>
            </button>
          </div>

          {/* Status indicators */}
          <div className="border-t pt-3 space-y-2" style={{ borderColor: colors.ui_border }}>
            <div className="flex items-center justify-between text-xs">
              <span style={{ color: colors.ui_text_dark }}>CPU Usage:</span>
              <span style={{ color: colors.ui_text }}>23%</span>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span style={{ color: colors.ui_text_dark }}>Memory:</span>
              <span style={{ color: colors.ui_text }}>1.2 GB</span>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span style={{ color: colors.ui_text_dark }}>Disk:</span>
              <span style={{ color: colors.ui_text }}>45 GB free</span>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span style={{ color: colors.ui_text_dark }}>FPS:</span>
              <span style={{ color: colors.success }}>60.0</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ControlsPanel;
