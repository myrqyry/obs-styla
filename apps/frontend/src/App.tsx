import React, { useState } from 'react';
import { ThemeEditor, ThemeVars } from './components/ThemeEditor';
import { ThemePreview } from './components/ThemePreview';
import { useQueryClient } from '@tanstack/react-query';
import MetaEditor from './MetaEditor';
import Converter from './Converter';
import DeleteIcon from './assets/delete.svg';
import DuplicateIcon from './assets/duplicate.svg';
import EditIcon from './assets/edit.svg';
import PreviewIcon from './assets/preview.svg';
import type {
   Theme,
   ThemeMeta,
   ValidationResponse
 } from './types/api';
import { useToast } from './hooks/useToast';
import { ToastContainer } from './components/Toast';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ValidationReport } from './components/ValidationReport';
import {
  useGetThemes,
  usePostGenerate,
  useGetValidate,
  useDeleteThemesFilename,
  usePostThemesFilenameDuplicate,
  useGetThemesFilenameMeta,
  usePostThemesFilenameMeta,
  getThemesFilenameMeta,
} from './services/orval';

interface EditingTheme {
  name: string;
  meta: ThemeMeta;
}


const DEFAULT_THEME_VARS: ThemeVars = {
  'primary-color': '#3b82f6',
  'secondary-color': '#8b5cf6',
  'background-color': '#1f2937',
  'text-color': '#f3f4f6',
  // Add more semantic/palette vars as needed
};

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'gen' | 'val' | 'conv'>('gen');
  const [genOutput, setGenOutput] = useState<string>('No generation run yet.');
  const [validationData, setValidationData] = useState<ValidationResponse | null>(null);
  const [editingTheme, setEditingTheme] = useState<EditingTheme | null>(null);
  const [themeVars, setThemeVars] = useState<ThemeVars>(DEFAULT_THEME_VARS);
  const { toasts, addToast, removeToast } = useToast();
  const queryClient = useQueryClient();

  const { data: themes = [], isLoading: themesLoading, error: themesError } = useGetThemes();

  const generateMutation = usePostGenerate({
    mutation: {
      onSuccess: (result) => {
        setGenOutput(JSON.stringify(result.results, null, 2));
        queryClient.invalidateQueries({ queryKey: ['themes'] });
        addToast('Generation completed successfully', 'success');
      },
      onError: (error: Error) => {
        setGenOutput(`Generation failed: ${error.message}`);
        addToast(error.message, 'error');
      },
    },
  });

  const {
    data: valData,
    isLoading: valLoading,
    error: valError,
    refetch: refetchValidate,
  } = useGetValidate(
    {},
    {
      enabled: false,
      onSuccess: (data) => {
        setValidationData(data);
        addToast('Validation completed', 'success');
      },
      onError: (error: Error) => {
        addToast(error.message, 'error');
      },
    }
  );

  const updateMetaMutation = usePostThemesFilenameMeta({
    mutation: {
      onSuccess: () => {
        addToast('Meta updated successfully', 'success');
      },
      onError: (error: Error) => {
        addToast(error.message, 'error');
      },
    },
  });

  const deleteMutation = useDeleteThemesFilename({
    mutation: {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['themes'] });
        addToast('Theme deleted successfully', 'success');
      },
      onError: (error: Error) => {
        addToast(error.message, 'error');
      },
    },
  });

  const duplicateMutation = usePostThemesFilenameDuplicate({
    mutation: {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['themes'] });
        addToast('Theme duplicated successfully', 'success');
      },
      onError: (error: Error) => {
        addToast(error.message, 'error');
      },
    },
  });

  const handleGenerate = () => {
    generateMutation.mutate();
  };

  const handleValidate = () => {
    setValidationData(null);
    refetchValidate();
  };

  const handleDelete = (themeName: string) => {
    if (!confirm(`Are you sure you want to delete ${themeName}?`)) return;
    deleteMutation.mutate({ filename: themeName });
  };

  const handleDuplicate = (themeName: string) => {
    const lastDotIndex = themeName.lastIndexOf('.');
    const baseName = lastDotIndex !== -1 ? themeName.substring(0, lastDotIndex) : themeName;
    const extension = lastDotIndex !== -1 ? themeName.substring(lastDotIndex + 1) : '';
    const newName = prompt(
      'Enter a new name for the duplicated theme:',
      `${baseName}-copy.${extension}`
    );

    if (!newName) return;

    duplicateMutation.mutate({ filename: themeName, data: { newName } });
  };

  const handleEdit = async (themeName: string) => {
    try {
      const data = await getThemesFilenameMeta({ filename: themeName });
      setEditingTheme({ name: themeName, meta: data });
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to fetch metadata';
      addToast(errorMsg, 'error');
    }
  };

  const isLoading = generateMutation.isPending || valLoading || deleteMutation.isPending || duplicateMutation.isPending || themesLoading;

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

      {themesError && (
        <div className="error-banner">
          <span>{themesError.message}</span>
          <button onClick={() => queryClient.invalidateQueries({ queryKey: ['themes'] })}>×</button>
        </div>
      )}

      <main>

        {activeTab === 'gen' && (
          <section id="gen" className="panel flex flex-col gap-6">
            <div className="controls flex gap-2">
              <button onClick={handleGenerate} disabled={isLoading}>
                {isLoading ? 'Running...' : 'Run Generation'}
              </button>
              <button onClick={() => queryClient.invalidateQueries({ queryKey: ['themes'] })} disabled={isLoading}>
                Refresh Themes
              </button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="font-semibold mb-2">Theme Editor</h3>
                <ThemeEditor vars={themeVars} onChange={setThemeVars} />
              </div>
              <div>
                <h3 className="font-semibold mb-2">Live Preview</h3>
                <ThemePreview vars={themeVars} />
              </div>
            </div>
            <div className="panel-inner mt-4">
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
            {validationData ? (
              <ValidationReport data={validationData} />
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
            queryClient.invalidateQueries({ queryKey: ['themes'] });
          }}
        />
      )}
    </div>
  );
};

export default App;