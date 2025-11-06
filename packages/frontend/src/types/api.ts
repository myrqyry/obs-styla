export interface ApiResponse<T = any> {
  success?: boolean;
  error?: string;
  data?: T;
}

export interface ThemeFile {
  name: string;
  path: string;
  size: number;
  modified: number;
  type: 'ovt' | 'obt' | 'json';
}

export interface ThemeListResponse {
  themes: ThemeFile[];
}

export interface ValidationError {
  code: string;
  message: string;
  line?: number;
  severity: 'error' | 'warning' | 'info';
}

export interface ThemeValidationReport {
  name: string;
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationError[];
  meta?: ThemeMeta;
}

export interface ValidationResponse {
  validations: ThemeValidationReport[];
  duplicate_ids: Array<{
    id: string;
    files: string[];
  }>;
}
