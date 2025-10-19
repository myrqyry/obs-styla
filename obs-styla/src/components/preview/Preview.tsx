import React, { useContext } from 'react';
import { ThemeContext } from '../../context/ThemeContext';
import ScenesPanel from './ScenesPanel';
import SourcesPanel from './SourcesPanel';
import ControlsPanel from './ControlsPanel';
import './Preview.css';

const Preview = () => {
  const { state } = useContext(ThemeContext);
  const { colors } = state;

  const style = {
    backgroundColor: colors.ui_background,
    color: colors.ui_text,
  };

  return (
    <div className="preview-container" style={style}>
      <div className="preview-header">
        {/* Mock header */}
      </div>
      <div className="preview-body">
        <div className="preview-scenes">
          <ScenesPanel />
        </div>
        <div className="preview-sources">
          <SourcesPanel />
        </div>
        <div className="preview-mixer">
          {/* Audio mixer will go here */}
          <h2>Audio Mixer</h2>
        </div>
        <div className="preview-controls">
          <ControlsPanel />
        </div>
      </div>
    </div>
  );
};

export default Preview;
