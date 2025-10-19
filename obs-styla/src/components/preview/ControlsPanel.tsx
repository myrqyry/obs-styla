import React, { useContext, useState } from 'react';
import { ThemeContext } from '../../context/ThemeContext';
import './Panel.css';

const ControlsPanel = () => {
  const { state } = useContext(ThemeContext);
  const { colors } = state;

  const buttonStyle = {
    backgroundColor: colors.button_background,
    color: colors.button_text,
    border: `1px solid ${colors.input_border}`,
  };

  const buttonHoverStyle = {
    backgroundColor: colors.button_background_hover,
  };

  const Button = ({ children }: { children: React.ReactNode }) => {
    const [hovered, setHovered] = useState(false);
    return (
      <button
        style={hovered ? { ...buttonStyle, ...buttonHoverStyle } : buttonStyle}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        {children}
      </button>
    );
  };

  return (
    <div className="panel">
      <div className="panel-header">Controls</div>
      <div className="panel-content">
        <div className="controls-grid">
          <Button>Start Streaming</Button>
          <Button>Start Recording</Button>
          <Button>Start Virtual Camera</Button>
          <Button>Start Replay Buffer</Button>
          <Button>Studio Mode</Button>
          <Button>Settings</Button>
          <Button>Exit</Button>
        </div>
      </div>
    </div>
  );
};

export default ControlsPanel;
