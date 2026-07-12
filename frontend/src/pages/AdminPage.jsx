import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { LayoutDashboard, LogOut, Pencil, PlusCircle, RefreshCw, Trash2 } from 'lucide-react';
import api, { getErrorMessage } from '../api';
import { useAuth } from '../AuthContext';

function AdminPage() {
  const [vehicles, setVehicles] = useState([]);
  const [form, setForm] = useState({ make: '', model: '', category: '', image_url: '', price: '', quantity: 0 });
  const [editingVehicle, setEditingVehicle] = useState(null); // stores vehicle being updated
  const [restockVehicleId, setRestockVehicleId] = useState(null); // stores vehicle ID being restocked
  const [restockQuantity, setRestockQuantity] = useState(1);
  const [loading, setLoading] = useState(false);
  const [formLoading, setFormLoading] = useState(false);
  const [actionLoadingId, setActionLoadingId] = useState(null);
  const [feedback, setFeedback] = useState({ type: '', message: '' });

  const { user, logout, isAdmin, canDelete, canRestock } = useAuth();

  const loadVehicles = async () => {
    setLoading(true);
    try {
      const response = await api.get('/api/vehicles');
      setVehicles(response.data);
    } catch (error) {
      setFeedback({ type: 'error', message: getErrorMessage(error) });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadVehicles();
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (formLoading) return;
    setFormLoading(true);
    setFeedback({ type: '', message: '' });
    try {
      await api.post('/api/vehicles', { ...form, price: String(form.price) });
      setForm({ make: '', model: '', category: '', image_url: '', price: '', quantity: 0 });
      setFeedback({ type: 'success', message: 'Vehicle added successfully to the catalog!' });
      loadVehicles();
    } catch (error) {
      setFeedback({ type: 'error', message: getErrorMessage(error) });
    } finally {
      setFormLoading(false);
    }
  };

  const handleUpdate = async (e) => {
    e.preventDefault();
    if (formLoading) return;
    setFormLoading(true);
    setFeedback({ type: '', message: '' });
    try {
      const response = await api.put(`/api/vehicles/${editingVehicle.id}`, {
        make: editingVehicle.make,
        model: editingVehicle.model,
        category: editingVehicle.category,
        image_url: editingVehicle.image_url,
        price: String(editingVehicle.price),
        quantity: editingVehicle.quantity,
      });
      setFeedback({ type: 'success', message: `Successfully updated ${response.data.make} ${response.data.model}!` });
      setEditingVehicle(null);
      loadVehicles();
    } catch (error) {
      setFeedback({ type: 'error', message: getErrorMessage(error) });
    } finally {
      setFormLoading(false);
    }
  };

  const handleRestock = async (e) => {
    e.preventDefault();
    if (formLoading) return;
    setFormLoading(true);
    setFeedback({ type: '', message: '' });
    try {
      const response = await api.post(`/api/vehicles/${restockVehicleId}/restock`, {
        quantity: parseInt(restockQuantity, 10),
      });
      setFeedback({ type: 'success', message: `Restocked successfully. New quantity: ${response.data.quantity}` });
      setRestockVehicleId(null);
      setRestockQuantity(1);
      loadVehicles();
    } catch (error) {
      setFeedback({ type: 'error', message: getErrorMessage(error) });
    } finally {
      setFormLoading(false);
    }
  };

  const handleDelete = async (id, make, model) => {
    if (!window.confirm(`Are you sure you want to permanently delete the ${make} ${model}?`)) {
      return;
    }
    setActionLoadingId(id);
    setFeedback({ type: '', message: '' });
    try {
      await api.delete(`/api/vehicles/${id}`);
      setFeedback({ type: 'success', message: `${make} ${model} removed from inventory.` });
      loadVehicles();
    } catch (error) {
      setFeedback({ type: 'error', message: getErrorMessage(error) });
    } finally {
      setActionLoadingId(null);
    }
  };

  return (
    <div className="dashboard-container">
      {/* Header bar */}
      <header className="header glass">
        <div className="brand-logo">
          <span className="logo-icon">🛠️</span>
          <div className="brand-info">
            <h2>AutoInventory</h2>
            <p className="subtitle">Management Console</p>
          </div>
        </div>

        <div className="user-profile">
          <div className="user-details">
            <span className="user-name">{user?.name}</span>
            <span className="user-role-badge font-role">{user?.role}</span>
          </div>
          <div className="action-buttons">
            <Link to="/dashboard" className="button button-secondary nav-btn">
              <LayoutDashboard size={14} />
              View Fleet
            </Link>
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
        </div>
      )}

      <div className="admin-grid">

        {/* Creation/Edit Form Section */}
        <section className="form-section">
          {editingVehicle ? (
            <div className="card glass edit-form-card">
              <div className="card-header-row">
                <h3>Edit Vehicle</h3>
                <button className="cancel-edit-btn" onClick={() => setEditingVehicle(null)}>Cancel</button>
              </div>
              <form className="form" onSubmit={handleUpdate}>
                <div className="form-group">
                  <label htmlFor="edit-make">Make</label>
                  <input
                    id="edit-make"
                    className="input"
                    value={editingVehicle.make}
                    onChange={(e) => setEditingVehicle({ ...editingVehicle, make: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="edit-model">Model</label>
                  <input
                    id="edit-model"
                    className="input"
                    value={editingVehicle.model}
                    onChange={(e) => setEditingVehicle({ ...editingVehicle, model: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="edit-category">Category</label>
                  <input
                    id="edit-category"
                    className="input"
                    value={editingVehicle.category}
                    onChange={(e) => setEditingVehicle({ ...editingVehicle, category: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="edit-image-url">Image URL</label>
                  <input
                    id="edit-image-url"
                    className="input"
                    placeholder="e.g. /images/ford-mustang.jpg or https://..."
                    value={editingVehicle.image_url || ''}
                    onChange={(e) => setEditingVehicle({ ...editingVehicle, image_url: e.target.value })}
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="edit-price">Price (₹)</label>
                  <input
                    id="edit-price"
                    type="number"
                    step="0.01"
                    className="input"
                    value={editingVehicle.price}
                    onChange={(e) => setEditingVehicle({ ...editingVehicle, price: e.target.value })}
                    required
                  />
                </div>
                <div className="form-group">
                  <label htmlFor="edit-quantity">Quantity</label>
                  <input
                    id="edit-quantity"
                    type="number"
                    className="input"
                    value={editingVehicle.quantity}
                    onChange={(e) => setEditingVehicle({ ...editingVehicle, quantity: parseInt(e.target.value, 10) })}
                    required
                  />
                </div>
                <button className="button button-primary" type="submit" disabled={formLoading}>
                  {formLoading ? 'Saving...' : 'Save Changes'}
                </button>
              </form>
            </div>
          ) : restockVehicleId ? (
            <div className="card glass restock-form-card">
              <div className="card-header-row">
                <h3>Restock Inventory</h3>
                <button className="cancel-edit-btn" onClick={() => setRestockVehicleId(null)}>Cancel</button>
              </div>
              <form className="form" onSubmit={handleRestock}>
                <div className="form-group">
                  <label htmlFor="restock-qty">Units to Add</label>
                  <input
                    id="restock-qty"
                    type="number"
                    min="1"
                    className="input"
                    value={restockQuantity}
                    onChange={(e) => setRestockQuantity(e.target.value)}
                    required
                  />
                </div>
                <button className="button button-primary" type="submit" disabled={formLoading}>
                  {formLoading ? 'Applying...' : 'Apply Restock'}
                </button>
              </form>
            </div>
          ) : (
            <div className="card glass add-form-card">
              <h3>
                <PlusCircle size={18} style={{ display: 'inline', marginRight: '8px', verticalAlign: 'middle' }} />
                Add New Vehicle
              </h3>
              <p className="subtitle">Publish a new car listing to the dealership catalog.</p>
              <form className="form" onSubmit={handleCreate}>
                <div className="grid grid-2">
                  <div className="form-group">
                    <label htmlFor="add-make">Make</label>
                    <input
                      id="add-make"
                      className="input"
                      placeholder="e.g. Ford"
                      value={form.make}
                      onChange={(e) => setForm({ ...form, make: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="add-model">Model</label>
                    <input
                      id="add-model"
                      className="input"
                      placeholder="e.g. Mustang"
                      value={form.model}
                      onChange={(e) => setForm({ ...form, model: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="add-category">Category</label>
                    <input
                      id="add-category"
                      className="input"
                      placeholder="e.g. Sports, Sedan"
                      value={form.category}
                      onChange={(e) => setForm({ ...form, category: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="add-image-url">Image URL</label>
                    <input
                      id="add-image-url"
                      className="input"
                      placeholder="e.g. /images/ford-mustang.jpg or https://..."
                      value={form.image_url}
                      onChange={(e) => setForm({ ...form, image_url: e.target.value })}
                    />
                  </div>
                  <div className="form-group">
                    <label htmlFor="add-price">Price (₹)</label>
                    <input
                      id="add-price"
                      type="number"
                      step="0.01"
                      className="input"
                      placeholder="0.00"
                      value={form.price}
                      onChange={(e) => setForm({ ...form, price: e.target.value })}
                      required
                    />
                  </div>
                </div>
                <div className="form-group">
                  <label htmlFor="add-quantity">Initial Stock Quantity</label>
                  <input
                    id="add-quantity"
                    type="number"
                    min="0"
                    className="input"
                    value={form.quantity}
                    onChange={(e) => setForm({ ...form, quantity: parseInt(e.target.value, 10) })}
                    required
                  />
                </div>
                <button className="button button-primary" type="submit" disabled={formLoading}>
                  {formLoading ? 'Publishing...' : 'Publish Vehicle'}
                </button>
              </form>
            </div>
          )}
        </section>

        {/* Administration Table / List Section */}
        <section className="catalog-section">
          <div className="section-header">
            <h3>Dealership Inventory Fleet</h3>
            {loading && <div className="loading-spinner-small">Reloading items...</div>}
          </div>

          <div className="admin-list-container">
            {vehicles.length === 0 && !loading ? (
              <div className="empty-state card glass">
                <h4>Catalog is Empty</h4>
                <p>No vehicles have been listed yet. Use the creation form to add the first vehicle.</p>
              </div>
            ) : (
              <div className="admin-table-wrapper">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Make &amp; Model</th>
                      <th>Category</th>
                      <th>Price</th>
                      <th>Quantity</th>
                      <th className="actions-header">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {vehicles.map((vehicle) => (
                      <tr key={vehicle.id} className={vehicle.quantity === 0 ? 'zero-stock-row' : ''}>
                        <td>#{vehicle.id}</td>
                        <td className="vehicle-name-cell">
                          <strong>{vehicle.make}</strong> {vehicle.model}
                        </td>
                        <td>
                          <span className="table-category-badge">{vehicle.category}</span>
                        </td>
                        <td className="price-cell">
                          ₹{parseFloat(vehicle.price).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                        </td>
                        <td>
                          <span className={`table-quantity ${vehicle.quantity === 0 ? 'zero' : ''}`}>
                            {vehicle.quantity} units
                          </span>
                        </td>
                        <td>
                          <div className="table-actions">
                            {/* Edit — available to ADMIN and SALESPERSON */}
                            <button
                              className="button button-secondary action-sm"
                              onClick={() => setEditingVehicle(vehicle)}
                              disabled={actionLoadingId === vehicle.id}
                            >
                              <Pencil size={13} />
                              Edit
                            </button>

                            {/* Restock — ADMIN only */}
                            {canRestock && (
                              <button
                                className="button button-secondary action-sm restock-action-btn"
                                onClick={() => setRestockVehicleId(vehicle.id)}
                                disabled={actionLoadingId === vehicle.id}
                                title="Add inventory units"
                              >
                                <RefreshCw size={13} />
                                Restock
                              </button>
                            )}

                            {/* Delete — ADMIN only */}
                            {canDelete && (
                              <button
                                className="button button-danger action-sm"
                                onClick={() => handleDelete(vehicle.id, vehicle.make, vehicle.model)}
                                disabled={actionLoadingId === vehicle.id}
                                title="Delete vehicle from records"
                              >
                                <Trash2 size={13} />
                                Delete
                              </button>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

export default AdminPage;
