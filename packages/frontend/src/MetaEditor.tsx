
import React, { useState } from 'react';
import axios from 'axios';

interface MetaEditorProps {
  themeName: string;
  initialMeta: any;
  onClose: () => void;
  onSave: () => void;
}

const MetaEditor: React.FC<MetaEditorProps> = ({ themeName, initialMeta, onClose, onSave }) => {
  const [meta, setMeta] = useState(initialMeta);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setMeta({
      ...meta,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post(`/api/themes/${encodeURIComponent(themeName)}/meta`, { meta });
      onSave();
    } catch (e: any) {
      alert(`Error saving metadata: ${String(e)}`);
    }
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <h3>Edit Metadata for {themeName}</h3>
        <form onSubmit={handleSubmit}>
          <label htmlFor="id">ID</label>
          <input type="text" id="id" name="id" value={meta.id || ''} onChange={handleChange} />
          <label htmlFor="name">Name</label>
          <input type="text" id="name" name="name" value={meta.name || ''} onChange={handleChange} />
          <label htmlFor="author">Author</label>
          <input type="text" id="author" name="author" value={meta.author || ''} onChange={handleChange} />
          <label htmlFor="version">Version</label>
          <input type="text" id="version" name="version" value={meta.version || ''} onChange={handleChange} />
          <label htmlFor="dark">Dark</label>
          <input type="checkbox" id="dark" name="dark" checked={meta.dark || false} onChange={handleChange} />
          <div className="modal-buttons">
            <button type="submit">Save</button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MetaEditor;
