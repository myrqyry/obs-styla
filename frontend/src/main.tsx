
import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';
import axios from 'axios';
import MetaEditor from './MetaEditor';
import './style.css';

const App = () => {
  const [themes, setThemes] = useState<Theme[]>([]);
  const [activeTab, setActiveTab] = useState('gen');
  const [genOutput, setGenOutput] = useState('No generation run yet.');
  const [valOutput, setValOutput] = useState('No validation run yet.');
  const [editingTheme, setEditingTheme] = useState<EditingTheme | null>(null);

  const listThemes = async () => {
    try {
      const r = await axios.get('/api/themes');
      setThemes(r.data.themes || []);
    } catch (e: any) {
      setThemes([]);
    }
  };

  useEffect(() => {
    listThemes();
  }, []);

  const handleGenerate = async () => {
    setGenOutput('Running generation scripts...');
    try {
      const r = await axios.post('/api/generate');
      setGenOutput(JSON.stringify(r.data.results, null, 2));
      listThemes();
    } catch (e: any) {
      setGenOutput(`Generation failed: ${String(e)}`);
    }
  };

  const handleValidate = async () => {
    setValOutput('Running validation...');
    try {
      const r = await axios.get('/api/validate');
      const data = r.data;
      let html = '';

      html += `<h3>Validation Summary</h3>`;
      html += `<ul>`;
      html += `<li>${data.validations.length} themes validated</li>`;
      html += `<li>${data.duplicate_ids.length} duplicate theme IDs found</li>`;
      html += `</ul>`;

      data.validations.forEach((v: any) => {
        html += `<div class="validation-report">`;
        html += `<h4>${v.name}</h4>`;
        if (v.error) {
          html += `<div class="error">Error: ${v.error}</div>`;
        } else {
          const report = v.report;
          html += `<ul>`;
          html += `<li><strong>Errors:</strong> ${report.summary.errors}</li>`;
          html += `<li><strong>Warnings:</strong> ${report.summary.warnings}</li>`;
          html += `</ul>`;

          if (report.errors.length > 0) {
            html += `<h5>Errors</h5>`;
            html += `<ul class="errors">`;
            report.errors.forEach((err: any) => {
              html += `<li><code>${err.code}</code>: ${err.message} (line ${err.line || 'N/A'})</li>`;
            });
            html += `</ul>`;
          }

          if (report.warnings.length > 0) {
            html += `<h5>Warnings</h5>`;
            html += `<ul class="warnings">`;
            report.warnings.forEach((warn: any) => {
              html += `<li><code>${warn.code}</code>: ${warn.message} (line ${warn.line || 'N/A'})</li>`;
            });
            html += `</ul>`;
          }
        }
        html += `</div>`;
      });

      setValOutput(html);
    } catch (e: any) {
      setValOutput(`Validation failed: ${String(e)}`);
    }
  };

  const handleDelete = async (themeName: string) => {
    if (confirm(`Are you sure you want to delete ${themeName}?`)) {
      try {
        await axios.delete(`/api/themes/${encodeURIComponent(themeName)}`);
        listThemes();
      } catch (e: any) {
        alert(`Error deleting theme: ${String(e)}`);
      }
    }
  };

  const handleDuplicate = async (themeName: string) => {
    const newName = prompt(`Enter a new name for the duplicated theme:`, `${themeName.split('.')[0]}-copy.ovt`);
    if (newName) {
      try {
        await axios.post(`/api/themes/${encodeURIComponent(themeName)}/duplicate`, { new_name: newName });
        listThemes();
      } catch (e: any) {
        alert(`Error duplicating theme: ${String(e)}`);
      }
    }
  };

  const handleEdit = async (themeName: string) => {
    try {
      const r = await axios.get(`/api/themes/${encodeURIComponent(themeName)}/meta`);
      setEditingTheme({ name: themeName, meta: r.data });
    } catch (e: any) {
      alert(`Error fetching metadata: ${String(e)}`);
    }
  };

  return (
    <div className="app">
      <header>
        <h1>OBS Styla</h1>
        <nav className="tabs">
          <button onClick={() => setActiveTab('gen')} className={activeTab === 'gen' ? 'active' : ''}>Generator</button>
          <button onClick={() => setActiveTab('val')} className={activeTab === 'val' ? 'active' : ''}>Validator</button>
        </nav>
      </header>
      <main>
        {activeTab === 'gen' && (
          <section id="gen" className="panel">
            <div className="controls">
              <button onClick={handleGenerate}>Run Generation</button>
              <button onClick={listThemes}>Refresh Themes</button>
            </div>
            <div className="panel-inner">{genOutput}</div>
            <h3>Generated Themes</h3>
            <ul id="themes-list">
              {themes.map((t) => (
                <li key={t.name}>
                  <a href={`/api/themes/${encodeURIComponent(t.name)}`} target="_blank">{t.name} ({t.size} bytes)</a>
                  <button onClick={() => handleDelete(t.name)}>Delete</button>
                  <button onClick={() => handleDuplicate(t.name)}>Duplicate</button>
                  <button onClick={() => handleEdit(t.name)}>Edit</button>
                  <button onClick={() => window.open(`/api/themes/${encodeURIComponent(t.name)}`, '_blank')}>Preview</button>
                </li>
              ))}
            </ul>
          </section>
        )}
        {activeTab === 'val' && (
          <section id="val" className="panel">
            <div className="controls">
              <button onClick={handleValidate}>Run Validation</button>
            </div>
            <div className="panel-inner" dangerouslySetInnerHTML={{ __html: valOutput }}></div>
          </section>
        )}
      </main>
      {editingTheme && (
        <MetaEditor
          themeName={editingTheme.name}
          initialMeta={editingTheme.meta}
          onClose={() => setEditingTheme(null)}
          onSave={() => {
            setEditingTheme(null);
            listThemes();
          }}
        />
      )}
    </div>
  );
};

const container = document.getElementById('root');
const root = createRoot(container!);
root.render(<App />);
