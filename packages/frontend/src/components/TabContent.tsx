import React from 'react';
import { useTabs } from '../contexts/TabContext';
import { useThemes } from '../hooks/useThemes';
import { ThemeList } from './ThemeList';
import axios from 'axios';

export const TabContent: React.FC = () => {
  const { activeTab } = useTabs();
  const { themes, refetch } = useThemes();
  const [genOutput, setGenOutput] = React.useState('No generation run yet.');
  const [valOutput, setValOutput] = React.useState('No validation run yet.');
  const [editingTheme, setEditingTheme] = React.useState<any | null>(null);


  const handleGenerate = async () => {
    setGenOutput('Running generation scripts...');
    try {
      const r = await axios.post('/api/generate');
      setGenOutput(JSON.stringify(r.data.results, null, 2));
      refetch();
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
        refetch();
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
        refetch();
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
    <>
      {activeTab === 'gen' && (
        <section id="gen" className="panel">
          <div className="controls">
            <button onClick={handleGenerate}>Run Generation</button>
            <button onClick={refetch}>Refresh Themes</button>
          </div>
          <div className="panel-inner"><pre>{genOutput}</pre></div>
          <ThemeList themes={themes} onDelete={handleDelete} onDuplicate={handleDuplicate} onEdit={handleEdit} />
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
    </>
  );
};
