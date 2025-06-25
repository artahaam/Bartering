// src/utils/api.js

import axios from 'axios';
import { getToken } from './auth';

// 1. Create a reusable axios instance with a base URL.
const api = axios.create({
  baseURL: 'http://localhost:8000/api', // All requests will be prefixed with this
});

// 2. Use an interceptor to automatically add the auth token to every request.
api.interceptors.request.use((config) => {
  const token = getToken();
  if (token) {
    // If a token exists, add it to the Authorization header.
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export default api;