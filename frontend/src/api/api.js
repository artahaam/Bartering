// src/api/api.js
import axios from 'axios';

// const API_BASE_URL = 'http://localhost:8000/api'; // Update with your Django server URL
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized (e.g., redirect to login)
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Add request interceptor to include auth token if exists
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// API endpoints
export const apiService = {
  // Authentication
  login: (credentials) => api.post('/auth/login/', credentials),
  register: (userData) => api.post('/auth/register/', userData),
  
  // Offers
  getOffers: () => api.get('/offers/'),
  createOffer: (offerData) => api.post('/offers/', offerData),
  getOfferDetail: (id) => api.get(`/offers/${id}/`),
  
  // Barters
  proposeBarter: (offerId, proposalData) => api.post(`/offers/${offerId}/propose/`, proposalData),
  getBarters: () => api.get('/barters/'),
  acceptBarter: (barterId) => api.patch(`/barters/${barterId}/accept/`),
  
  // User
  getUserProfile: () => api.get('/users/me/'),
};