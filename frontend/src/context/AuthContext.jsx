// src/context/AuthContext.jsx
import { createContext, useContext, useState, useEffect } from 'react';
import { apiService } from '../api/api';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadUser() {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const response = await apiService.getUserProfile();
          setUser(response.data);
        }
      } catch (error) {
        console.error('Error loading user', error);
        logout();
      } finally {
        setLoading(false);
      }
    }
    loadUser();
  }, []);

  const login = async (credentials) => {
    const response = await apiService.login(credentials);
    localStorage.setItem('access_token', response.data.access);
    const userResponse = await apiService.getUserProfile();
    setUser(userResponse.data);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}