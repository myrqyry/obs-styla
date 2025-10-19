import React from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Preview from './components/preview/Preview';
import ThemeUploader from './components/ThemeUploader';
import ThemeExporter from './components/ThemeExporter';
import './App.css';

function App() {
  return (
    <ThemeProvider>
      <div className="App">
        <h1>OBS Styla</h1>
        <div className="main-content">
          <div className="theme-controls">
            <ThemeUploader />
            <hr />
            <ThemeExporter />
          </div>
          <div className="preview-area">
            <Preview />
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
