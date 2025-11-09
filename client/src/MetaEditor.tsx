import React, { useState, useEffect } from 'react';
import api from './services/api';
import { useToast } from './hooks/useToast';
import type { ThemeMeta } from './types/api';
import './MetaEditor.css';

interface MetaEditorProps {
  themeName: string;
  initialMeta: ThemeMeta;
  onClose: () => void;
  onSave: () => void;
}

interface ValidationErrors {
  id?: string;
  name?: string;
  author?: string;
  version?: string;
}

const MetaEditor: React.FC<MetaEditorProps> = ({
   themeName,
   initialMeta,
   onClose,
   onSave
 }) => {
  const [meta, setMeta] = useState<ThemeMeta>(initialMeta);
  const [errors, setErrors] = useState<ValidationErrors>({});
  const [isSaving, setIsSaving] = useState(false);
  const { addToast } = useToast();

  const validateField = (name: keyof ThemeMeta, value: string | boolean): string | null => {
    if (typeof value === 'boolean') return null;

    switch (name) {
      case 'id':
        if (!value.trim()) return 'ID is required';
        if (!/^[a-z0-9-_]+$/i.test(value)) {
          return 'ID can only contain letters, numbers, hyphens, and underscores';
        }
        if (value.length < 3) return 'ID must be at least 3 characters';
        if (value.length > 50) return 'ID must be less than 50 characters';
        break;
      case 'name':
        if (!value.trim()) return 'Name is required';
        if (value.length < 3) return 'Name must be at least 3 characters';
        if (value.length > 100) return 'Name must be less than 100 characters';
        break;
      case 'author':
        if (!value.trim()) return 'Author is required';
        if (value.length > 100) return 'Author must be less than 100 characters';
        break;
      case 'version':
        if (!value.trim()) return 'Version is required';
        if (!/^\d+\.\d+\.\d+$/.test(value)) {
          return 'Version must follow semantic versioning (e.g., 1.0.0)';
        }
        break;
    }

    return null;
  };

  const validateForm = (): boolean => {
    const newErrors: ValidationErrors = {};

    const idError = validateField('id', meta.id);
    if (idError) newErrors.id = idError;

    const nameError = validateField('name', meta.name);
    if (nameError) newErrors.name = nameError;

    const authorError = validateField('author', meta.author);
    if (authorError) newErrors.author = authorError;

    const versionError = validateField('version', meta.version);
    if (versionError) newErrors.version = versionError;

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value, type, checked } = e.target;
    const newValue = type === 'checkbox' ? checked : value;

    setMeta({
      ...meta,
      [name]: newValue,
    });

    // Clear error for this field when user types
    if (errors[name as keyof ValidationErrors]) {
      setErrors({
        ...errors,
        [name]: undefined,
      });
    }
  };

  const handleBlur = (e: React.FocusEvent<HTMLInputElement>): void => {
    const { name, value } = e.target;
    const error = validateField(name as keyof ThemeMeta, value);

    if (error) {
      setErrors({
        ...errors,
        [name]: error,
      });
    }
  };

  const handleSubmit = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();

    if (!validateForm()) {
      addToast('Please fix validation errors', 'error');
      return;
    }

    setIsSaving(true);
    try {
      await api.updateThemeMeta(themeName, meta);
      addToast('Metadata saved successfully', 'success');
      onSave();
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : 'Failed to save metadata';
      addToast(errorMsg, 'error');
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = useCallback((): void => {
    if (JSON.stringify(meta) !== JSON.stringify(initialMeta)) {
      if (!confirm('You have unsaved changes. Are you sure you want to close?')) {
        return;
      }
    }
    onClose();
  }, [meta, initialMeta, onClose]);

  // Close on Escape key
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent): void => {
      if (e.key === 'Escape') {
        handleCancel();
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, [handleCancel]);

  return (
    <div className="modal-overlay" onClick={handleCancel}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h3>Edit Theme Metadata</h3>
          <button
             className="modal-close"
             onClick={handleCancel}
            aria-label="Close modal"
          >
            ×
          </button>
        </div>

        <div className="modal-info">
          <span className="theme-name">{themeName}</span>
        </div>

        <form onSubmit={handleSubmit} noValidate>
          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="id">
                Theme ID <span className="required">*</span>
              </label>
              <input
                type="text"
                id="id"
                name="id"
                value={meta.id}
                onChange={handleChange}
                onBlur={handleBlur}
                className={errors.id ? 'error' : ''}
                disabled={isSaving}
                placeholder="my-theme-id"
                required
              />
              {errors.id && <span className="error-message">{errors.id}</span>}
              <span className="field-hint">
                Unique identifier using only letters, numbers, hyphens, and underscores
              </span>
            </div>

            <div className="form-group">
              <label htmlFor="name">
                Display Name <span className="required">*</span>
              </label>
              <input
                type="text"
                id="name"
                name="name"
                value={meta.name}
                onChange={handleChange}
                onBlur={handleBlur}
                className={errors.name ? 'error' : ''}
                disabled={isSaving}
                placeholder="My Beautiful Theme"
                required
              />
              {errors.name && <span className="error-message">{errors.name}</span>}
              <span className="field-hint">
                Human-readable theme name displayed in OBS Studio
              </span>
            </div>

            <div className="form-group">
              <label htmlFor="author">
                Author <span className="required">*</span>
              </label>
              <input
                type="text"
                id="author"
                name="author"
                value={meta.author}
                onChange={handleChange}
                onBlur={handleBlur}
                className={errors.author ? 'error' : ''}
                disabled={isSaving}
                placeholder="Your Name"
                required
              />
              {errors.author && <span className="error-message">{errors.author}</span>}
              <span className="field-hint">Theme creator name</span>
            </div>

            <div className="form-group">
              <label htmlFor="version">
                Version <span className="required">*</span>
              </label>
              <input
                type="text"
                id="version"
                name="version"
                value={meta.version}
                onChange={handleChange}
                onBlur={handleBlur}
                className={errors.version ? 'error' : ''}
                disabled={isSaving}
                placeholder="1.0.0"
                required
              />
              {errors.version && <span className="error-message">{errors.version}</span>}
              <span className="field-hint">
                Semantic version number (major.minor.patch)
              </span>
            </div>

            <div className="form-group checkbox-group">
              <label htmlFor="dark" className="checkbox-label">
                <input
                  type="checkbox"
                  id="dark"
                  name="dark"
                  checked={meta.dark}
                  onChange={handleChange}
                  disabled={isSaving}
                />
                <span>Dark theme</span>
              </label>
              <span className="field-hint">
                Enable if this theme uses dark colors
              </span>
            </div>
          </div>

          <div className="modal-footer">
            <button
               type="button"
               className="btn-secondary"
               onClick={handleCancel}
              disabled={isSaving}
            >
              Cancel
            </button>
            <button
               type="submit"
               className="btn-primary"
              disabled={isSaving}
            >
              {isSaving ? 'Saving...' : 'Save Changes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MetaEditor;
