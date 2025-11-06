import axios from 'axios';
import { Theme } from '../types/theme';

const getThemes = async (): Promise<Theme[]> => {
  const response = await axios.get('/api/themes');
  return response.data.themes || [];
};

export const themeService = {
  getThemes,
};
