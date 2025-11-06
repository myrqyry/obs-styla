import React from 'react';
import { useTabs } from '../contexts/TabContext';

export const Header: React.FC = () => {
  const { activeTab, setActiveTab } = useTabs();

  return (
    <header>
      <h1>OBS Styla</h1>
      <nav className="tabs">
        <button onClick={() => setActiveTab('gen')} className={activeTab === 'gen' ? 'active' : ''}>Generator</button>
        <button onClick={() => setActiveTab('val')} className={activeTab === 'val' ? 'active' : ''}>Validator</button>
      </nav>
    </header>
  );
};
