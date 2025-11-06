import { ThemeFile } from './api';

export interface ThemeMeta {
  name: string;
  id: string;
  extends?: string;
  author: string;
  dark: boolean;
  version?: string;
  description?: string;
}

export interface ThemeColors {
  [key: string]: string;
}

export interface Theme extends ThemeFile {
  meta: ThemeMeta;
  colors: ThemeColors;
  styles: string;
}
