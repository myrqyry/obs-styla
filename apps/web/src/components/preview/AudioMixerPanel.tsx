import React, { useContext } from 'react';
import { ThemeContext } from '../../context/ThemeContext';

interface VolumeMeterProps {
  level: number;
  peak: number;
  label: string;
  muted?: boolean;
}

const VolumeMeter: React.FC<VolumeMeterProps> = ({ level, peak, label, muted = false }) => {
  const { state } = useContext(ThemeContext);
  const { colors } = state;

  const getBarColor = (value: number) => {
    if (muted) return colors.ui_text_dark;
    if (value > 0.8) return colors.volumemeter_peak;
    if (value > 0.6) return colors.volumemeter_warning;
    return colors.volumemeter_good;
  };

  return (
    <div className="flex items-center space-x-2 py-1">
      <div className="w-16 text-xs truncate" style={{ color: colors.ui_text_dark }}>
        {label}
      </div>
      <div className="flex-1 flex items-center space-x-1">
        <div className="flex-1 h-4 bg-gray-800 rounded-sm overflow-hidden relative">
          {/* Background bars */}
          <div className="absolute inset-0 flex">
            {Array.from({ length: 20 }, (_, i) => (
              <div
                key={i}
                className="flex-1 mx-px rounded-sm"
                style={{
                  backgroundColor: i < level * 20 ? getBarColor(level) : colors.ui_background_dark,
                  opacity: i < level * 20 ? 1 : 0.3
                }}
              />
            ))}
          </div>
          {/* Peak indicator */}
          {peak > 0 && (
            <div
              className="absolute top-0 w-0.5 h-full"
              style={{
                left: `${peak * 100}%`,
                backgroundColor: colors.volumemeter_peak,
                boxShadow: `0 0 4px ${colors.volumemeter_peak}`
              }}
            />
          )}
        </div>
        <div className="w-8 text-xs text-center" style={{ color: colors.ui_text_dark }}>
          {muted ? 'M' : `${Math.round(level * 100)}%`}
        </div>
      </div>
    </div>
  );
};

const AudioMixerPanel = () => {
  const { state } = useContext(ThemeContext);
  const { colors } = state;

  // Simulate audio levels
  const audioSources = [
    { name: 'Desktop Audio', level: 0.7, peak: 0.85, muted: false },
    { name: 'Mic/Aux', level: 0.3, peak: 0.4, muted: false },
    { name: 'Media Source', level: 0.9, peak: 0.95, muted: true },
    { name: 'Browser Source', level: 0.2, peak: 0.25, muted: false },
  ];

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
        Audio Mixer
      </div>
      <div className="flex-1 p-3 overflow-y-auto space-y-3">
        {audioSources.map((source, index) => (
          <div key={index} className="space-y-2">
            <VolumeMeter
              level={source.level}
              peak={source.peak}
              label={source.name}
              muted={source.muted}
            />
            <div className="flex items-center justify-between px-2">
              <div className="flex items-center space-x-1">
                <button
                  className={`w-6 h-6 rounded flex items-center justify-center text-xs ${
                    source.muted ? 'bg-red-500' : 'hover:bg-gray-600'
                  }`}
                  style={{
                    backgroundColor: source.muted ? colors.error : 'transparent',
                    color: source.muted ? 'white' : colors.ui_text
                  }}
                >
                  {source.muted ? '🔇' : '🔊'}
                </button>
                <button
                  className="w-6 h-6 rounded flex items-center justify-center text-xs hover:bg-gray-600"
                  style={{ color: colors.ui_text }}
                >
                  ⚙️
                </button>
              </div>
              <div className="flex items-center space-x-1">
                <input
                  type="range"
                  min="-60"
                  max="0"
                  defaultValue="-10"
                  className="w-16 h-1 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
                  style={{
                    background: `linear-gradient(to right, ${colors.accent} 0%, ${colors.accent} 70%, ${colors.ui_background_dark} 70%, ${colors.ui_background_dark} 100%)`
                  }}
                />
                <span className="w-8 text-xs text-right" style={{ color: colors.ui_text_dark }}>
                  -10dB
                </span>
              </div>
            </div>
          </div>
        ))}

        {/* Master volume */}
        <div className="border-t pt-3 mt-3" style={{ borderColor: colors.ui_border }}>
          <VolumeMeter
            level={0.6}
            peak={0.75}
            label="Master"
            muted={false}
          />
          <div className="flex items-center justify-center mt-2">
            <input
              type="range"
              min="-60"
              max="0"
              defaultValue="-5"
              className="w-32 h-2 bg-gray-600 rounded-lg appearance-none cursor-pointer slider"
              style={{
                background: `linear-gradient(to right, ${colors.accent} 0%, ${colors.accent} 75%, ${colors.ui_background_dark} 75%, ${colors.ui_background_dark} 100%)`
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default AudioMixerPanel;