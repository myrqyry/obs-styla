import React from 'react';
import { ThemeProvider } from './context/ThemeContext';
import Preview from './components/preview/Preview';
import ThemeUploader from './components/ThemeUploader';
import ThemeExporter from './components/ThemeExporter';

function App() {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-background text-foreground p-6">
        <h1 className="text-center text-3xl font-bold mb-6">OBS Styla</h1>
        <div className="grid grid-cols-[300px_1fr] gap-6 h-[calc(100vh-120px)]">
          <div className="border border-border rounded-lg p-3">
            <ThemeUploader />
            <hr className="my-4 border-border" />
            <ThemeExporter />
          </div>
          <div className="flex items-center justify-center">
            <Preview />
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;
