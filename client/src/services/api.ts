import axios, { AxiosError, AxiosInstance, AxiosRequestConfig } from 'axios';
import type {
  Theme,
  ThemeMeta,
  ThemesResponse,
  GenerateResponse,
  ValidationResponse,
  ConvertRequest,
  ConvertResponse,
} from '../types/api';

class ApiService {
  private client: AxiosInstance;

  constructor(baseURL: string = '/api') {
    this.client = axios.create({
      baseURL,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add timestamp to prevent caching
        if (config.method === 'get') {
          config.params = {
            ...config.params,
            _t: Date.now(),
          };
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response) {
          // Server responded with error
          const message = (error.response.data as any)?.error || error.message;
          throw new Error(message);
        } else if (error.request) {
          // Request made but no response
          throw new Error('No response from server. Please check your connection.');
        } else {
          // Something else happened
          throw new Error(error.message);
        }
      }
    );
  }

  // Themes
  async getThemes(): Promise<Theme[]> {
    const { data } = await this.client.get<ThemesResponse>('/themes');
    return data.themes || [];
  }

  async downloadTheme(filename: string): string {
    return `/api/themes/${encodeURIComponent(filename)}`;
  }

  async deleteTheme(filename: string): Promise<void> {
    await this.client.delete(`/themes/${encodeURIComponent(filename)}`);
  }

  async duplicateTheme(filename: string, newName: string): Promise<void> {
    await this.client.post(`/themes/${encodeURIComponent(filename)}/duplicate`, {
      new_name: newName,
    });
  }

  // Theme metadata
  async getThemeMeta(filename: string): Promise<ThemeMeta> {
    const { data } = await this.client.get<ThemeMeta>(
      `/themes/${encodeURIComponent(filename)}/meta`
    );
    return data;
  }

  async updateThemeMeta(filename: string, meta: Partial<ThemeMeta>): Promise<void> {
    await this.client.post(`/themes/${encodeURIComponent(filename)}/meta`, { meta });
  }

  // Generation
  async generateThemes(): Promise<GenerateResponse> {
    const { data } = await this.client.post<GenerateResponse>('/generate');
    return data;
  }

  // Validation
  async validateThemes(): Promise<ValidationResponse> {
    const { data } = await this.client.get<ValidationResponse>('/validate');
    return data;
  }

  // Conversion
  async convertJsonToOvt(json: string): Promise<string> {
    const { data } = await this.client.post<ConvertResponse>('/convert', { json });
    return data.ovt;
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      await this.client.get('/health');
      return true;
    } catch {
      return false;
    }
  }
}

export const api = new ApiService();
export default api;
