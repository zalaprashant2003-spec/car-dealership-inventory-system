import React, { useEffect, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { LayoutDashboard, LogOut, Search, ShoppingCart, Settings, X } from 'lucide-react';
import api, { getErrorMessage } from '../api';
import { useAuth } from '../AuthContext';

function DashboardPage() {
  const [vehicles, setVehicles] = useState([]);
  const [searchParams, setSearchParams] = useState({
    make: '',
    model: '',
    category: '',
    price_min: '',
    price_max: '',
  });
  const [loading, setLoading] = useState(false);
  const [feedback, setFeedback] = useState({ type: '', message: '' });

  const { user, logout, canManageVehicles } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Show success message passed from BillingPage after a confirmed purchase
  useEffect(() => {
    if (location.state?.successMessage) {
      setFeedback({ type: 'success', message: location.state.successMessage });
      // Clear so back-navigation doesn't re-show it
      window.history.replaceState({}, document.title);
    }
  }, [location.state]);

  const fetchVehicles = async (filters = {}) => {
    setLoading(true);
    setFeedback((prev) => (prev.type === 'success' ? prev : { type: '', message: '' }));
    try {
      const queryParams = new URLSearchParams();
      Object.entries(filters).forEach(([key, val]) => {
        if (val) queryParams.append(key, val);
      });

      const response = await api.get(`/api/vehicles?${queryParams.toString()}`);
      setVehicles(response.data);
    } catch (error) {
      setFeedback({ type: 'error', message: getErrorMessage(error) });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchVehicles();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchVehicles(searchParams);
  };

  const handleReset = () => {
    const cleared = { make: '', model: '', category: '', price_min: '', price_max: '' };
    setSearchParams(cleared);
    fetchVehicles(cleared);
  };

  // Navigate to billing page with vehicle data — no API call here
  const handlePurchaseClick = (vehicle) => {
    navigate('/billing', { state: { vehicle } });
  };

  return (
    <div className="dashboard-container">
      {/* Header bar */}
      <header className="header glass">
        <div className="brand-logo">
          <span className="logo-icon">🚗</span>
          <div className="brand-info">
            <h2>AutoInventory</h2>
            <p className="subtitle">Dealership Control Panel</p>
          </div>
        </div>

        <div className="user-profile">
          <div className="user-details">
            <span className="user-name">{user?.name}</span>
            <span className="user-role-badge">{user?.role}</span>
          </div>
          <div className="action-buttons">
            {canManageVehicles && (
              <Link to="/admin" className="button button-secondary nav-btn">
                <Settings size={14} />
                Management
              </Link>
            )}
            <button className="button button-danger nav-btn" onClick={logout}>
              <LogOut size={14} />
              Sign Out
            </button>
          </div>
        </div>
      </header>

      {/* Alert Banner */}
      {feedback.message && (
        <div className={`feedback-alert ${feedback.type === 'success' ? 'success' : 'error'}`}>
          {feedback.message}
          <button className="alert-close-btn" onClick={() => setFeedback({ type: '', message: '' })}>
            <X size={16} />
          </button>
        </div>
      )}

      {/* Main Content layout */}
      <div className="dashboard-content">

        {/* Advanced Filters Card */}
        <aside className="filters-card card glass">
          <h3>
            <Search size={16} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
            Advanced Search
          </h3>
          <p className="filter-desc">Filter vehicles in real-time by properties and price range.</p>

          <form onSubmit={handleSearch} className="filter-form">
            <div className="filter-group">
              <label htmlFor="filter-make">Make</label>
              <input
                id="filter-make"
                className="input"
                placeholder="e.g. Toyota"
                value={searchParams.make}
                onChange={(e) => setSearchParams({ ...searchParams, make: e.target.value })}
              />
            </div>

            <div className="filter-group">
              <label htmlFor="filter-model">Model</label>
              <input
                id="filter-model"
                className="input"
                placeholder="e.g. Corolla"
                value={searchParams.model}
                onChange={(e) => setSearchParams({ ...searchParams, model: e.target.value })}
              />
            </div>

            <div className="filter-group">
              <label htmlFor="filter-category">Category</label>
              <input
                id="filter-category"
                className="input"
                placeholder="e.g. Sedan, SUV"
                value={searchParams.category}
                onChange={(e) => setSearchParams({ ...searchParams, category: e.target.value })}
              />
            </div>

            <div className="filter-group">
              <label>Price Range</label>
              <div className="range-inputs">
                <input
                  type="number"
                  className="input price-input"
                  placeholder="Min (₹)"
                  value={searchParams.price_min}
                  onChange={(e) => setSearchParams({ ...searchParams, price_min: e.target.value })}
                />
                <span className="range-separator">to</span>
                <input
                  type="number"
                  className="input price-input"
                  placeholder="Max (₹)"
                  value={searchParams.price_max}
                  onChange={(e) => setSearchParams({ ...searchParams, price_max: e.target.value })}
                />
              </div>
            </div>

            <div className="filter-actions">
              <button className="button button-primary" type="submit" disabled={loading}>
                <Search size={14} />
                Apply Search
              </button>
              <button
                className="button button-secondary"
                type="button"
                onClick={handleReset}
                disabled={loading}
              >
                Reset Filters
              </button>
            </div>
          </form>
        </aside>

        {/* Inventory Listing */}
        <main className="inventory-section">
          <div className="section-header">
            <h3>
              <LayoutDashboard size={18} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
              Available Fleet ({vehicles.length})
            </h3>
            {loading && <div className="loading-spinner-small">Updating catalog...</div>}
          </div>

          {vehicles.length === 0 && !loading ? (
            <div className="empty-state card glass">
              <div className="empty-icon">🔍</div>
              <h4>No Vehicles Found</h4>
              <p>No vehicles in stock match your search filters. Try widening your criteria.</p>
              <button className="button button-secondary" onClick={handleReset}>
                View All Vehicles
              </button>
            </div>
          ) : (
            <div className="grid grid-2">
              {vehicles.map((vehicle) => {
                const isOutOfStock = vehicle.quantity === 0;

                return (
                  <article key={vehicle.id} className={`vehicle-card card glass ${isOutOfStock ? 'out-of-stock-card' : ''}`}>
                    <div className="card-badge-container">
                      <span className="category-badge">{vehicle.category}</span>
                      {isOutOfStock ? (
                        <span className="status-badge error">Out of Stock</span>
                      ) : (
                        <span className="status-badge success">In Stock</span>
                      )}
                    </div>

                    <h3 className="vehicle-title">
                      {vehicle.make} <span className="highlight-model">{vehicle.model}</span>
                    </h3>

                    <div className="vehicle-stats">
                      <div className="stat">
                        <span className="stat-label">Retail Price</span>
                        <span className="stat-value price">₹{parseFloat(vehicle.price).toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
                      </div>
                      <div className="stat">
                        <span className="stat-label">Stock Quantity</span>
                        <span className={`stat-value quantity ${isOutOfStock ? 'danger' : ''}`}>
                          {vehicle.quantity} units
                        </span>
                      </div>
                    </div>

                    <button
                      className="button button-primary purchase-btn"
                      disabled={isOutOfStock}
                      onClick={() => handlePurchaseClick(vehicle)}
                    >
                      <ShoppingCart size={16} />
                      {isOutOfStock ? 'Sold Out' : 'Purchase Unit'}
                    </button>
                  </article>
                );
              })}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

export default DashboardPage;
