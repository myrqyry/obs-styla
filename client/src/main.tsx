import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import MetaEditor from './MetaEditor';
import Converter from './Converter';
import { ReactComponent as DeleteIcon } from './assets/delete.svg';
import { ReactComponent as DuplicateIcon } from './assets/duplicate.svg';
import { ReactComponent as EditIcon } from './assets/edit.svg';
import { ReactComponent as PreviewIcon } from './assets/preview.svg';
import type {
   Theme,
   ThemeMeta,
   ValidationResponse
 } from './types/api';
import { useToast } from './hooks/useToast';
import { ToastContainer } from './components/Toast';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ValidationReport } from './components/ValidationReport';
import api from './services/api';
import './style.css';

interface EditingTheme {
  name: string;
  meta: ThemeMeta;
}

const App: React.FC = () => {
  const [themes, setThemes] = useState<Theme[]>([]);
  const [activeTab, setActiveTab] = useState<'gen' | 'val' | 'conv'>('gen');
  const [genOutput, setGenOutput] = useState<string>('No generation run yet.');
  const [valData, setValData] = useState<ValidationResponse | null>(null);
  const [editingTheme, setEditingTheme] = useState<EditingTheme | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const { toasts, addToast, removeToast } = useToast();

   const listThemes = async (): Promise<void> => {
    try {
      setIsLoading(true);
      setError(null);
      const themes = await api.getThemes();
      setThemes(themes);
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to fetch themes';
      setError(errorMsg);
      setThemes([]);
    } finally {
      setIsLoading(false);
    }
  };

   useEffect(() => {
    listThemes();
  }, []);

   const handleGenerate = async (): Promise<void> => {
    setIsLoading(true);
    try {
      const result = await api.generateThemes();
      setGenOutput(JSON.stringify(result.results, null, 2));
      await listThemes();
      addToast('Generation completed successfully', 'success');
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Generation failed';
      setGenOutput(`Generation failed: ${errorMsg}`);
      addToast(errorMsg, 'error');
    } finally {
      setIsLoading(false);
    }
  };

   const handleValidate = async (): Promise<void> => {
    setIsLoading(true);
    setValData(null);

     try {
      const data = await api.validateThemes();
      setValData(data);
      addToast('Validation completed', 'success');
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Validation failed';
      addToast(errorMsg, 'error');
    } finally {
      setIsLoading(false);
    }
  };

   const handleDelete = async (themeName: string): Promise<void> => {
    if (!confirm(`Are you sure you want to delete ${themeName}?`)) return;

     try {
      await api.deleteTheme(themeName);
      await listThemes();
      addToast('Theme deleted successfully', 'success');
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to delete theme';
      addToast(errorMsg, 'error');
    }
  };

   const handleDuplicate = async (themeName: string): Promise<void> => {
    const lastDotIndex = themeName.lastIndexOf('.');
    const baseName = lastDotIndex !== -1 ? themeName.substring(0, lastDotIndex) : themeName;
    const newName = prompt(
      'Enter a new name for the duplicated theme:',
       `${baseName}-copy.${extension}`
    );

     if (!newName) return;

     try {
      await api.duplicateTheme(themeName, newName);
      await listThemes();
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to duplicate theme';
      addToast(errorMsg, 'error');
    }
  };

   const handleEdit = async (themeName: string): Promise<void> => {
    try {
      const data = await api.getThemeMeta(themeName);
      setEditingTheme({ name: themeName, meta: data });
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to fetch metadata';
      addToast(errorMsg, 'error');
    }
  };

   return (
    <div className="app">
      {isLoading && <LoadingSpinner overlay message="Processing..." />}
      <ToastContainer toasts={toasts} onClose={removeToast} />
      <header>
        <h1>OBS Styla</h1>
        <nav className="tabs">
          <button
             onClick={() => setActiveTab('gen')}
             className={activeTab === 'gen' ? 'active' : ''}
            disabled={isLoading}
          >
            Generator
          </button>
          <button
             onClick={() => setActiveTab('val')}
             className={activeTab === 'val' ? 'active' : ''}
            disabled={isLoading}
          >
            Validator
          </button>
          <button
             onClick={() => setActiveTab('conv')}
             className={activeTab === 'conv' ? 'active' : ''}
            disabled={isLoading}
          >
            Converter
          </button>
        </nav>
      </header>

       {error && (
        <div className="error-banner">
          <span>{error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

       <main>
        {activeTab === 'gen' && (
          <section id="gen" className="panel">
            <div className="controls">
              <button onClick={handleGenerate} disabled={isLoading}>
                {isLoading ? 'Running...' : 'Run Generation'}
              </button>
              <button onClick={listThemes} disabled={isLoading}>
                Refresh Themes
              </button>
            </div>
            <div className="panel-inner">
              <pre>{genOutput}</pre>
            </div>
            <h3>Generated Themes ({themes.length})</h3>
            {themes.length === 0 ? (
              <p className="empty-state">No themes generated yet.</p>
            ) : (
              <ul id="themes-list">
                {themes.map((t) => (
                  <li key={t.name}>
                    <a
                       href={api.downloadTheme(t.name)}
                       target="_blank"
                       rel="noopener noreferrer"
                    >
                      {t.name} ({(t.size / 1024).toFixed(2)} KB)
                    </a>
                    <div className="theme-actions">
                      <button
                         onClick={() => handleEdit(t.name)}
                         title="Edit metadata"
                        aria-label={`Edit ${t.name}`}
                      >
                        <EditIcon />
                      </button>
                      <button
                         onClick={() => handleDuplicate(t.name)}
                         title="Duplicate theme"
                        aria-label={`Duplicate ${t.name}`}
                      >
                        <DuplicateIcon />
                      </button>
                      <button
                         onClick={() => window.open(api.downloadTheme(t.name), '_blank')}
                         title="Preview theme"
                        aria-label={`Preview ${t.name}`}
                      >
                        <PreviewIcon />
                      </button>
                      <button
                         onClick={() => handleDelete(t.name)}
                         title="Delete theme"
                        aria-label={`Delete ${t.name}`}
                        className="danger"
                      >
                        <DeleteIcon />
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        )}

         {activeTab === 'val' && (
          <section id="val" className="panel">
            <div className="controls">
              <button onClick={handleValidate} disabled={isLoading}>
                {isLoading ? 'Validating...' : 'Run Validation'}
              </button>
            </div>
            {valData ? (
              <ValidationReport data={valData} />
            ) : (
              <p className="empty-state">No validation results yet. Click "Run Validation" to start.</p>
            )}
          </section>
        )}

         {activeTab === 'conv' && (
          <section id="conv" className="panel">
            <Converter />
          </section>
        )}
      </main>

       {editingTheme && (
        <MetaEditor
          themeName={editingTheme.name}
          initialMeta={editingTheme.meta}
          onClose={() => setEditingTheme(null)}
          onSave={async () => {
            setEditingTheme(null);
            await listThemes();
          }}
        />
      )}
    </div>
  );
};

 const container = document.getElementById('root');
if (!container) throw new Error('Root element not found');
const root = createRoot(container);
root.render(<App />);
