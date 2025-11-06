import React from 'react';
import { TabProvider } from './contexts/TabContext';
import { Header } from './components/Header';
import { TabContent } from './components/TabContent';
import { ErrorBoundary } from './components/ErrorBoundary';

export const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <TabProvider>
        <div className="app">
          <Header />
          <main className="main-content">
            <TabContent />
          </main>
        </div>
      </TabProvider>
    </ErrorBoundary>
  );
};
