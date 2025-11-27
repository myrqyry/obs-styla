import React, { useContext, useState, useEffect } from 'react';
import { ThemeContext } from '../../context/ThemeContext';
import ScenesPanel from './ScenesPanel';
import SourcesPanel from './SourcesPanel';
import ControlsPanel from './ControlsPanel';
import AudioMixerPanel from './AudioMixerPanel';

const Preview = () => {
  const { state } = useContext(ThemeContext);
  const { colors } = state;

  // Simulate OBS states
  const [isRecording, setIsRecording] = useState(false);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isVirtualCam, setIsVirtualCam] = useState(false);
  const [studioMode, setStudioMode] = useState(false);

  const style = {
    backgroundColor: colors.ui_background,
    color: colors.ui_text,
    borderColor: colors.ui_border,
  };

  return (
    <div className="flex flex-col w-full h-full border rounded-lg overflow-hidden font-sans shadow-lg" style={style}>
      {/* OBS-style title bar */}
      <div
        className="h-8 flex items-center justify-between px-3 border-b text-sm font-medium"
        style={{
          backgroundColor: colors.header_background,
          borderColor: colors.ui_border,
          color: colors.ui_text
        }}
      >
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 rounded-full bg-red-500"></div>
          <span>OBS Studio - Preview</span>
        </div>
        <div className="flex items-center space-x-1">
          {/* Status indicators */}
          {isRecording && (
            <div className="flex items-center space-x-1 px-2 py-1 rounded text-xs font-bold animate-pulse"
                 style={{ backgroundColor: colors.error, color: colors.ui_background }}>
              <div className="w-2 h-2 rounded-full bg-white animate-pulse"></div>
              REC
            </div>
          )}
          {isStreaming && (
            <div className="flex items-center space-x-1 px-2 py-1 rounded text-xs font-bold"
                 style={{ backgroundColor: colors.success, color: colors.ui_background }}>
              <div className="w-2 h-2 rounded-full bg-white"></div>
              LIVE
            </div>
          )}
          {isVirtualCam && (
            <div className="flex items-center space-x-1 px-2 py-1 rounded text-xs font-bold"
                 style={{ backgroundColor: colors.info, color: colors.ui_background }}>
              <div className="w-2 h-2 rounded-full bg-white"></div>
              VCAM
            </div>
          )}
        </div>
      </div>

      {/* Main content area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left sidebar - Scenes and Sources */}
        <div className="flex flex-col w-64 border-r" style={{ borderColor: colors.ui_border }}>
          <ScenesPanel />
          <div className="h-px" style={{ backgroundColor: colors.ui_border }}></div>
          <SourcesPanel />
        </div>

        {/* Center - Preview area */}
        <div className="flex-1 flex flex-col">
          {/* Preview header */}
          <div className="h-10 flex items-center justify-between px-4 border-b"
               style={{
                 backgroundColor: colors.dock_background,
                 borderColor: colors.ui_border,
                 color: colors.ui_text
               }}>
            <div className="flex items-center space-x-4">
              <span className="font-medium">Program</span>
              {studioMode && <span className="text-xs px-2 py-1 rounded" style={{ backgroundColor: colors.accent, color: colors.accent_text }}>Studio Mode</span>}
            </div>
            <div className="flex items-center space-x-2 text-xs">
              <span>1920x1080 @ 60fps</span>
              <span>•</span>
              <span>00:15:32</span>
            </div>
          </div>

          {/* Simulated video preview */}
          <div className="flex-1 relative bg-black">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="w-32 h-24 mx-auto mb-4 rounded border-2 border-dashed opacity-50"
                     style={{ borderColor: colors.ui_text_dark }}>
                  <div className="w-full h-full flex items-center justify-center">
                    <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clipRule="evenodd" />
                    </svg>
                  </div>
                </div>
                <p className="text-sm opacity-75" style={{ color: colors.ui_text_dark }}>
                  Video Preview Area
                </p>
                <p className="text-xs opacity-50" style={{ color: colors.ui_text_dark }}>
                  1920 × 1080 (16:9)
                </p>
              </div>
            </div>

            {/* Preview overlay controls */}
            <div className="absolute top-4 left-4 flex space-x-2">
              <button className="w-8 h-8 rounded flex items-center justify-center text-xs font-bold"
                      style={{
                        backgroundColor: colors.button_background,
                        color: colors.button_text,
                        border: `1px solid ${colors.ui_border}`
                      }}>
                🎯
              </button>
              <button className="w-8 h-8 rounded flex items-center justify-center text-xs font-bold"
                      style={{
                        backgroundColor: colors.button_background,
                        color: colors.button_text,
                        border: `1px solid ${colors.ui_border}`
                      }}>
                📐
              </button>
            </div>
          </div>
        </div>

        {/* Right sidebar - Audio Mixer and Controls */}
        <div className="flex flex-col w-80 border-l" style={{ borderColor: colors.ui_border }}>
          <AudioMixerPanel />
          <div className="h-px" style={{ backgroundColor: colors.ui_border }}></div>
          <ControlsPanel
            isRecording={isRecording}
            isStreaming={isStreaming}
            isVirtualCam={isVirtualCam}
            studioMode={studioMode}
            onRecordingChange={setIsRecording}
            onStreamingChange={setIsStreaming}
            onVirtualCamChange={setIsVirtualCam}
            onStudioModeChange={setStudioMode}
          />
        </div>
      </div>
    </div>
  );
};

export default Preview;
