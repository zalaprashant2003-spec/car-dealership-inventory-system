import axios from 'axios';

const api = axios.create({
  baseURL: '', // Empty base URL, handled by Vite proxy in development
});

// Interceptor to attach the JWT token to every request
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor to handle common response errors, like token expiration
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // If we get an Unauthorized response, clear token and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.dispatchEvent(new Event('auth:changed'));
      
      // Only redirect if we're not already on login or register page
      const path = window.location.pathname;
      if (path !== '/login' && path !== '/register') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const getErrorMessage = (error) => {
  if (!error) return 'An unknown error occurred';
  const detail = error.response?.data?.detail;
  if (typeof detail === 'string') return detail;
  if (Array.isArray(detail)) {
    // Format FastAPI Pydantic validation error lists (type, loc, msg, input, ctx)
    return detail
      .map((err) => {
        const fieldName = err.loc && err.loc.length > 1 ? err.loc[err.loc.length - 1] : '';
        const fieldLabel = fieldName ? `"${fieldName}" ` : '';
        return `${fieldLabel}${err.msg}`;
      })
      .join(', ');
  }
  return error.response?.data?.message || error.message || 'An unexpected error occurred';
};

export default api;

