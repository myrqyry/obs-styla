import React from 'react';
import type { ValidationResponse, ThemeValidation, ValidationReport as ValidationReportType } from '../types/api';
import './ValidationReport.css';

interface ValidationReportProps {
  data: ValidationResponse;
}

const ValidationReportItem: React.FC<{ validation: ThemeValidation }> = ({ validation }) => {
  if (validation.error) {
    return (
      <div className="validation-item validation-error">
        <h4>{validation.name}</h4>
        <div className="error-message">
          <strong>Error:</strong> {validation.error}
        </div>
      </div>
    );
  }

   if (!validation.report) return null;

   const { report } = validation;
  const hasIssues = report.errors.length > 0 || report.warnings.length > 0;

   return (
    <div className={`validation-item ${hasIssues ? 'has-issues' : 'success'}`}>
      <h4>
        {validation.name}
        <span className="validation-badge">
          {report.summary.errors === 0 && report.summary.warnings === 0 ? '✓' : '⚠'}
        </span>
      </h4>

       <div className="validation-summary">
        <span className={`summary-item ${report.summary.errors > 0 ? 'has-errors' : ''}`}>
          Errors: {report.summary.errors}
        </span>
        <span className={`summary-item ${report.summary.warnings > 0 ? 'has-warnings' : ''}`}>
          Warnings: {report.summary.warnings}
        </span>
      </div>

       {report.errors.length > 0 && (
        <div className="validation-issues">
          <h5>Errors</h5>
          <ul className="issues-list errors-list">
            {report.errors.map((err, idx) => (
              <li key={idx}>
                <code className="issue-code">{err.code}</code>
                <span className="issue-message">{err.message}</span>
                {err.line && <span className="issue-line">Line {err.line}</span>}
              </li>
            ))}
          </ul>
        </div>
      )}

       {report.warnings.length > 0 && (
        <div className="validation-issues">
          <h5>Warnings</h5>
          <ul className="issues-list warnings-list">
            {report.warnings.map((warn, idx) => (
              <li key={idx}>
                <code className="issue-code">{warn.code}</code>
                <span className="issue-message">{warn.message}</span>
                {warn.line && <span className="issue-line">Line {warn.line}</span>}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export const ValidationReport: React.FC<ValidationReportProps> = ({ data }) => {
  const totalThemes = data.validations.length;
  const themesWithErrors = data.validations.filter(v =>
     v.report && v.report.summary.errors > 0
  ).length;
  const themesWithWarnings = data.validations.filter(v =>
     v.report && v.report.summary.warnings > 0
  ).length;

   return (
    <div className="validation-report">
      <div className="validation-header">
        <h3>Validation Summary</h3>
        <div className="validation-stats">
          <div className="stat">
            <span className="stat-value">{totalThemes}</span>
            <span className="stat-label">Themes Validated</span>
          </div>
          <div className="stat error">
            <span className="stat-value">{themesWithErrors}</span>
            <span className="stat-label">With Errors</span>
          </div>
          <div className="stat warning">
            <span className="stat-value">{themesWithWarnings}</span>
            <span className="stat-label">With Warnings</span>
          </div>
          {data.duplicate_ids.length > 0 && (
            <div className="stat duplicate">
              <span className="stat-value">{data.duplicate_ids.length}</span>
              <span className="stat-label">Duplicate IDs</span>
            </div>
          )}
        </div>
      </div>

       {data.duplicate_ids.length > 0 && (
        <div className="duplicate-ids-section">
          <h4>Duplicate Theme IDs</h4>
          {data.duplicate_ids.map((dup, idx) => (
            <div key={idx} className="duplicate-group">
              <strong>ID: {dup.id}</strong>
              <ul>
                {dup.files.map((file, fileIdx) => (
                  <li key={fileIdx}>{file}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}

       <div className="validation-items">
        {data.validations.map((validation, idx) => (
          <ValidationReportItem key={idx} validation={validation} />
        ))}
      </div>
    </div>
  );
};
