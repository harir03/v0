import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data: { email: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data),
  
  login: (data: { username: string; password: string }) =>
    api.post('/auth/login', data, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }),
  
  me: () => api.get('/auth/me'),
};

// Agents API
export const agentsAPI = {
  list: () => api.get('/agents/'),
  
  get: (id: string) => api.get(`/agents/${id}`),
  
  create: (data: { name: string; description?: string; type: string; configuration?: any }) =>
    api.post('/agents/', data),
  
  update: (id: string, data: Partial<{ name: string; description?: string; type: string; configuration?: any }>) =>
    api.put(`/agents/${id}`, data),
  
  delete: (id: string) => api.delete(`/agents/${id}`),
  
  execute: (id: string, task: { type: string; data: any }) =>
    api.post(`/agents/${id}/execute`, task),
};