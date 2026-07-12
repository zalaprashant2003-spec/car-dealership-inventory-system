import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import api, { getErrorMessage } from '../api';
import { useAuth } from '../AuthContext';

function RegisterPage() {
  const [form, setForm] = useState({ name: '', email: '', password: '', role: 'CUSTOMER' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const response = await api.post('/api/auth/register', form);
      login(response.data);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="auth-container">
      <div className="auth-card card glass">
        <div className="brand-header">
          <div className="logo-icon">🚗</div>
          <h1>Car Dealership</h1>
          <p className="subtitle">Inventory Management System</p>
        </div>
        
        <h2>Create Account</h2>
        <p className="auth-desc">Register to access the dealer inventory dashboard.</p>

        {error && <div className="error-alert">{error}</div>}

        <form className="form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Full Name</label>
            <input
              id="name"
              className="input"
              placeholder="John Doe"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Email Address</label>
            <input
              id="email"
              type="email"
              className="input"
              placeholder="name@dealership.com"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password (8+ characters)</label>
            <input
              id="password"
              type="password"
              className="input"
              placeholder="••••••••"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="role">Workplace Role</label>
            <select
              id="role"
              className="select"
              value={form.role}
              onChange={(e) => setForm({ ...form, role: e.target.value })}
            >
              <option value="CUSTOMER">Customer</option>
              <option value="SALESPERSON">Salesperson</option>
              <option value="ADMIN">Admin</option>
            </select>
          </div>

          <button 
            className="button button-primary auth-btn" 
            type="submit" 
            disabled={loading}
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </button>
        </form>

        <div className="auth-footer">
          <p className="small">
            Already have an account? <Link to="/login" className="link-highlight">Login here</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
