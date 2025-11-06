import { useState, useEffect } from 'react';
import { themeService } from '../services/themeService';
import { Theme } from '../types/theme';

export const useThemes = () => {
  const [themes, setThemes] = useState<Theme[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchThemes = async () => {
    setLoading(true);
    setError(null);
    try {
      const fetchedThemes = await themeService.getThemes();
      setThemes(fetchedThemes);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch themes');
      setThemes([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchThemes();
  }, []);

  return {
    themes,
    loading,
    error,
    refetch: fetchThemes
  };
};
