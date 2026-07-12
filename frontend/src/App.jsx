import React, { useEffect } from 'react';
import { Navigate, Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import AdminPage from './pages/AdminPage';
import BillingPage from './pages/BillingPage';
import DashboardPage from './pages/DashboardPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';

function App() {
  const { token, canManageVehicles } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const publicPaths = ['/login', '/register'];
    const isPublicPath = publicPaths.includes(location.pathname);

    if (!token && !isPublicPath) {
      navigate('/login', { replace: true });
    } else if (token && isPublicPath) {
      navigate('/dashboard', { replace: true });
    }
  }, [location.pathname, token, navigate]);

  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/dashboard"
        element={token ? <DashboardPage /> : <Navigate to="/login" replace />}
      />
      <Route
        path="/admin"
        element={
          token ? (
            canManageVehicles ? (
              <AdminPage />
            ) : (
              <Navigate to="/dashboard" replace />
            )
          ) : (
            <Navigate to="/login" replace />
          )
        }
      />
      <Route
        path="/billing"
        element={token ? <BillingPage /> : <Navigate to="/login" replace />}
      />
      <Route path="*" element={<Navigate to={token ? '/dashboard' : '/login'} replace />} />
    </Routes>
  );
}

export default App;
