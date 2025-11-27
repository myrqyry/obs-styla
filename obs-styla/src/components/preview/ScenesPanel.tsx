import React from 'react';
import ListItem from './ListItem';
import './Panel.css';

const ScenesPanel = () => {
  return (
    <div className="panel">
      <div className="panel-header">Scenes</div>
      <div className="panel-content">
        <ul>
          <ListItem active>Starting Soon</ListItem>
          <ListItem>Main Scene</ListItem>
          <ListItem>Be Right Back</ListItem>
        </ul>
      </div>
    </div>
  );
};

export default ScenesPanel;
