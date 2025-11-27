import React, { useState, useEffect } from 'react';
import { usePostConvert } from './services/orval';
import { useToast } from './hooks/useToast';
import './Converter.css';

interface JsonValidationResult {
  valid: boolean;
  error?: string;
  errorPosition?: number;
}

const EXAMPLE_TEMPLATE = `{
  "meta": {
    "id": "my-custom-theme",
    "name": "My Custom Theme",
    "author": "Your Name",
    "version": "1.0.0",
    "dark": true
  },
  "vars": {
    "primary-color": "#3b82f6",
    "secondary-color": "#8b5cf6",
    "background-color": "#1f2937",
    "text-color": "#f3f4f6",
    "border-radius": "8px"
  }
}`;

const Converter: React.FC = () => {
  const [jsonInput, setJsonInput] = useState('');
  const [ovtOutput, setOvtOutput] = useState('');
  const [validation, setValidation] = useState<JsonValidationResult>({ valid: true });
  const { addToast } = useToast();

  const convertMutation = usePostConvert({
    mutation: {
      onSuccess: (result) => {
        setOvtOutput(result);
        addToast('Conversion successful!', 'success');
      },
      onError: (error: Error) => {
        setOvtOutput(`Conversion failed: ${error.message}`);
        addToast(error.message, 'error');
      },
    },
  });

  useEffect(() => {
    // Validate JSON as user types (debounced)
    const timer = setTimeout(() => {
      if (!jsonInput.trim()) {
        setValidation({ valid: true });
        return;
      }

      try {
        const parsed = JSON.parse(jsonInput);

        // Check structure
        if (!parsed.meta || !parsed.vars) {
          setValidation({
            valid: false,
            error: 'JSON must contain "meta" and "vars" objects',
          });
          return;
        }

        setValidation({ valid: true });
      } catch (err) {
        const error = err as Error;
        const match = error.message.match(/position (\d+)/);
        const lineNumber = match ? parseInt(match[1], 10) : undefined;

        setValidation({
          valid: false,
          error: error.message,
          lineNumber,
        });
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [jsonInput]);

  const handleConvert = (): void => {
    if (!validation.valid) {
      addToast('Please fix JSON errors before converting', 'error');
      return;
    }

    if (!jsonInput.trim()) {
      addToast('Please enter JSON to convert', 'warning');
      return;
    }

    convertMutation.mutate({ data: { json: jsonInput } });
  };

  const handleLoadExample = (): void => {
    setJsonInput(EXAMPLE_TEMPLATE);
    setOvtOutput('');
    addToast('Example template loaded', 'info');
  };

  const handleClear = (): void => {
    setJsonInput('');
    setOvtOutput('');
    setValidation({ valid: true });
  };

  const handleCopyOutput = async (): Promise<void> => {
    if (!ovtOutput) {
      addToast('Nothing to copy', 'warning');
      return;
    }

    try {
      await navigator.clipboard.writeText(ovtOutput);
      addToast('Copied to clipboard!', 'success');
    } catch {
      addToast('Failed to copy to clipboard', 'error');
    }
  };

  const handleDownload = (): void => {
    if (!ovtOutput) {
      addToast('Nothing to download', 'warning');
      return;
    }

    const blob = new Blob([ovtOutput], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'theme.ovt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    addToast('Downloaded theme.ovt', 'success');
  };

  return (
    <div className="converter">
      <div className="converter-header">
        <h3>JSON to OVT Converter</h3>
        <p className="converter-description">
          Convert JSON theme definitions to OBS Studio .ovt theme files
        </p>
      </div>

      <div className="converter-layout">
        <div className="converter-section">
          <div className="section-header">
            <h4>JSON Input</h4>
            <div className="section-actions">
              <button
                 className="btn-secondary btn-sm"
                 onClick={handleLoadExample}
                disabled={convertMutation.isPending}
              >
                Load Example
              </button>
              <button
                 className="btn-secondary btn-sm"
                 onClick={handleClear}
                disabled={convertMutation.isPending || !jsonInput}
              >
                Clear
              </button>
            </div>
          </div>

          <textarea
            className={`converter-input ${!validation.valid ? 'error' : ''}`}
            value={jsonInput}
            onChange={(e) => setJsonInput(e.target.value)}
            placeholder="Paste your JSON theme configuration here..."
            spellCheck={false}
            disabled={convertMutation.isPending}
          />

          {!validation.valid && validation.error && (
            <div className="validation-error">
              <strong>JSON Error:</strong> {validation.error}
              {validation.lineNumber && ` (near position ${validation.lineNumber})`}
            </div>
          )}

          <div className="convert-controls">
            <button
               className="btn-primary"
               onClick={handleConvert}
              disabled={!validation.valid || !jsonInput.trim() || convertMutation.isPending}
            >
              {convertMutation.isPending ? 'Converting...' : 'Convert to OVT'}
            </button>
          </div>
        </div>

        <div className="converter-divider" />

        <div className="converter-section">
          <div className="section-header">
            <h4>OVT Output</h4>
            <div className="section-actions">
              <button
                 className="btn-secondary btn-sm"
                 onClick={handleCopyOutput}
                disabled={!ovtOutput}
              >
                Copy
              </button>
              <button
                 className="btn-secondary btn-sm"
                 onClick={handleDownload}
                disabled={!ovtOutput}
              >
                Download
              </button>
            </div>
          </div>

          <textarea
            className="converter-output"
            value={ovtOutput}
            readOnly
            placeholder="OVT output will appear here after conversion..."
            spellCheck={false}
          />

          {ovtOutput && (
            <div className="output-info">
              <span>✓ Ready to use in OBS Studio</span>
            </div>
          )}
        </div>
      </div>

      <div className="converter-help">
        <h4>Format Requirements</h4>
        <ul>
          <li>JSON must include <code>meta</code> object with theme metadata</li>
          <li>JSON must include <code>vars</code> object with CSS variables</li>
          <li>All CSS variable names will be prefixed with <code>--</code> automatically</li>
        </ul>
      </div>
    </div>
  );
};

export default Converter;
