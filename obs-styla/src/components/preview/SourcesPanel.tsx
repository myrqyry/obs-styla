import React from 'react';
import ListItem from './ListItem';
import './Panel.css';

const SourcesPanel = () => {
  return (
    <div className="panel">
      <div className="panel-header">Sources</div>
      <div className="panel-content">
        <ul>
          <ListItem><span role="img" aria-label="desktop">🖥️</span> Desktop Capture</ListItem>
          <ListItem><span role="img" aria-label="camera">📷</span> Webcam</ListItem>
        </ul>
      </div>
    </div>
  );
};

export default SourcesPanel;
