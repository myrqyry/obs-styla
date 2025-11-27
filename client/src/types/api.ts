export interface Theme {
  name: string;
  path: string;
  size: number;
  modified: number;
}

export interface ThemeMeta {
  id: string;
  name: string;
  author: string;
  version: string;
  dark: boolean;
}

export interface ValidationError {
  code: string;
  message: string;
  line?: number;
}

export interface ValidationWarning {
  code: string;
  message: string;
  line?: number;
}

export interface ValidationReport {
  summary: {
    errors: number;
    warnings: number;
  };
  errors: ValidationError[];
  warnings: ValidationWarning[];
}

export interface ThemeValidation {
  name: string;
  report?: ValidationReport;
  error?: string;
}

export interface ApiResponse<T> {
  data: T;
  error?: string;
}

export interface ThemesResponse {
  themes: Theme[];
}

export interface GenerationResult {
  script: string;
  returncode?: number;
  stdout?: string;
  stderr?: string;
  status?: string;
  error?: string;
}

export interface GenerateResponse {
  results: GenerationResult[];
  themes: Theme[];
}

export interface ValidationResponse {
  validations: ThemeValidation[];
  duplicate_ids: Array<{
    id: string;
    files: string[];
  }>;
}

export interface ConvertRequest {
  json: string;
}

export interface ConvertResponse {
  ovt: string;
}
