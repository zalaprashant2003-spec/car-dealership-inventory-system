import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [user, setUser] = useState(() => {
    const storedUser = localStorage.getItem('user');
    try {
      return storedUser ? JSON.parse(storedUser) : null;
    } catch {
      return null;
    }
  });

  const navigate = useNavigate();

  // Keep state in sync with localStorage updates (from other tabs or interceptors)
  useEffect(() => {
    const handleAuthChange = () => {
      const storedToken = localStorage.getItem('token');
      const storedUser = localStorage.getItem('user');
      setToken(storedToken);
      try {
        setUser(storedUser ? JSON.parse(storedUser) : null);
      } catch {
        setUser(null);
      }
    };

    window.addEventListener('storage', handleAuthChange);
    window.addEventListener('auth:changed', handleAuthChange);

    return () => {
      window.removeEventListener('storage', handleAuthChange);
      window.removeEventListener('auth:changed', handleAuthChange);
    };
  }, []);

  const login = (userData) => {
    localStorage.setItem('token', userData.access_token);
    // Remove token from user data to avoid redundancy
    const { access_token, token_type, ...profile } = userData;
    localStorage.setItem('user', JSON.stringify(profile));
    setToken(userData.access_token);
    setUser(profile);
    window.dispatchEvent(new Event('auth:changed'));
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
    window.dispatchEvent(new Event('auth:changed'));
    navigate('/login', { replace: true });
  };

  const isAdmin = user?.role === 'ADMIN';
  const isSalesperson = user?.role === 'SALESPERSON';
  const isCustomer = user?.role === 'CUSTOMER';
  const canManageVehicles = isAdmin || isSalesperson;  // can add / edit
  const canDelete = isAdmin;
  const canRestock = isAdmin;

  return (
    <AuthContext.Provider value={{ token, user, login, logout, isAdmin, isSalesperson, isCustomer, canManageVehicles, canDelete, canRestock }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
