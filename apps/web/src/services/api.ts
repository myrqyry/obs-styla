import axios from 'axios';

export const customInstance = axios.create({
  baseURL: '/api',
});

export const apiMutator = (config: any) => {
  return customInstance(config);
};