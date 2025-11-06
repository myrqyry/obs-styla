import axios, { AxiosResponse } from 'axios';
import {
   ApiResponse,
   ThemeListResponse,
   ValidationResponse,
  ThemeFile
 } from '../types/api';

class ApiClient {
  private baseURL: string;

  constructor(baseURL = '/api') {
    this.baseURL = baseURL;
  }

  async getThemes(): Promise<ThemeFile[]> {
    const response: AxiosResponse<ThemeListResponse> = await axios.get(
      `${this.baseURL}/themes`
    );
    return response.data.themes;
  }

  async deleteTheme(filename: string): Promise<void> {
    await axios.delete(`${this.baseURL}/themes/${encodeURIComponent(filename)}`);
  }

  async duplicateTheme(filename: string, newName: string): Promise<void> {
    await axios.post(
      `${this.baseURL}/themes/${encodeURIComponent(filename)}/duplicate`,
      { new_name: newName }
    );
  }

  async validateThemes(): Promise<ValidationResponse> {
    const response: AxiosResponse<ValidationResponse> = await axios.get(
      `${this.baseURL}/validate`
    );
    return response.data;
  }

  async generateThemes(): Promise<any> {
    const response = await axios.post(`${this.baseURL}/generate`);
    return response.data;
  }
}

export const apiClient = new ApiClient();
