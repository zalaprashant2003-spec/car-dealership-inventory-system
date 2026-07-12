/**
 * BillingPage — Invoice confirmation screen.
 *
 * Receives vehicle data from DashboardPage via React Router location.state.
 * - Confirm Purchase: calls POST /api/vehicles/{id}/purchase, then navigates
 *   back to /dashboard with a success message.
 * - Cancel Purchase: navigates back to /dashboard without any API call.
 *
 * If opened directly (no router state), automatically redirects to /dashboard.
 */
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { ArrowLeft, CheckCircle, FileText, Printer, XCircle } from 'lucide-react';
import api, { getErrorMessage } from '../api';
import { useAuth } from '../AuthContext';

/** Generate a human-readable invoice number based on timestamp + vehicle id. */
function generateInvoiceNumber(vehicleId) {
  const now = new Date();
  const datePart = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, '0'),
    String(now.getDate()).padStart(2, '0'),
  ].join('');
  const timePart = String(now.getHours()).padStart(2, '0') + String(now.getMinutes()).padStart(2, '0');
  return `INV-${datePart}-${timePart}-${String(vehicleId).padStart(4, '0')}`;
}

function BillingPage() {
  const { state } = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [purchasing, setPurchasing] = useState(false);
  const [error, setError] = useState('');

  const [quantity, setQuantity] = useState(1);

  // Guard: if navigated to directly without vehicle state, redirect to dashboard
  const vehicle = state?.vehicle;
  if (!vehicle) {
    navigate('/dashboard', { replace: true });
    return null;
  }

  const invoiceNumber = generateInvoiceNumber(vehicle.id);
  const invoiceDate = new Date().toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
  const unitPrice = parseFloat(vehicle.price);
  const totalAmount = unitPrice * quantity;

  const handleConfirm = async () => {
    setPurchasing(true);
    setError('');
    try {
      await api.post(`/api/vehicles/${vehicle.id}/purchase`, { quantity: quantity });
      navigate('/dashboard', {
        replace: true,
        state: {
          successMessage: `✅ Successfully purchased ${quantity} unit(s) of ${vehicle.make} ${vehicle.model}! Invoice: ${invoiceNumber}`,
        },
      });
    } catch (err) {
      setError(getErrorMessage(err));
      setPurchasing(false);
    }
  };

  const handleCancel = () => {
    navigate('/dashboard', { replace: true });
  };

  return (
    <div className="billing-container">
      <div className="invoice-card card glass">

        {/* Invoice Header */}
        <div className="invoice-header">
          <div className="invoice-branding">
            <div className="invoice-logo">🚗</div>
            <div>
              <h1 className="invoice-company">AutoInventory</h1>
              <p className="invoice-tagline">Car Dealership Management System</p>
            </div>
          </div>
          <div className="invoice-meta">
            <div className="invoice-title-block">
              <FileText size={20} />
              <span>PURCHASE INVOICE</span>
            </div>
            <div className="invoice-number">{invoiceNumber}</div>
            <div className="invoice-date">{invoiceDate}</div>
          </div>
        </div>

        <div className="invoice-divider" />

        {/* Customer & Dealer Info */}
        <div className="invoice-parties">
          <div className="invoice-party">
            <div className="party-label">Bill To</div>
            <div className="party-name">{user?.name || 'Valued Customer'}</div>
            <div className="party-detail">{user?.email}</div>
            <div className="party-role-badge">{user?.role}</div>
          </div>
          <div className="invoice-party invoice-party-right">
            <div className="party-label">From</div>
            <div className="party-name">AutoInventory Dealership</div>
            <div className="party-detail">Premium Vehicle Sales</div>
          </div>
        </div>

        <div className="invoice-divider" />

        {/* Item Table */}
        <div className="invoice-items">
          <table className="invoice-table">
            <thead>
              <tr>
                <th>Vehicle</th>
                <th>Category</th>
                <th>Qty</th>
                <th className="text-right">Unit Price</th>
                <th className="text-right">Total</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <div className="invoice-vehicle-name">
                    <strong>{vehicle.make}</strong> {vehicle.model}
                  </div>
                </td>
                <td>
                  <span className="invoice-category-badge">{vehicle.category}</span>
                </td>
                <td>
                  <input
                    type="number"
                    min="1"
                    max={vehicle.quantity}
                    value={quantity}
                    onChange={(e) => {
                      const val = parseInt(e.target.value, 10);
                      if (!isNaN(val)) {
                        setQuantity(Math.min(Math.max(1, val), vehicle.quantity));
                      } else {
                        setQuantity(1);
                      }
                    }}
                    className="input"
                    style={{ width: '80px', padding: '4px' }}
                  />
                </td>
                <td className="text-right invoice-price">
                  ₹{unitPrice.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </td>
                <td className="text-right invoice-price">
                  ₹{totalAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Total Section */}
        <div className="invoice-total-section">
          <div className="invoice-total-row">
            <span className="invoice-total-label">Subtotal</span>
            <span>₹{totalAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}</span>
          </div>
          <div className="invoice-total-row">
            <span className="invoice-total-label">Tax</span>
            <span>Included</span>
          </div>
          <div className="invoice-divider" />
          <div className="invoice-total-row invoice-grand-total">
            <span>Total Amount Due</span>
            <span className="invoice-grand-amount">
              ₹{totalAmount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
            </span>
          </div>
        </div>

        {/* Stock Availability */}
        <div className="invoice-availability">
          <span className="availability-label">Stock Available:</span>
          <span className={`availability-value ${vehicle.quantity <= 1 ? 'low-stock' : ''}`}>
            {vehicle.quantity} unit{vehicle.quantity !== 1 ? 's' : ''}
          </span>
        </div>

        {/* Error banner */}
        {error && (
          <div className="error-alert invoice-error">
            {error}
          </div>
        )}

        {/* Action Buttons */}
        <div className="invoice-actions">
          <button
            className="button button-danger invoice-cancel-btn"
            onClick={handleCancel}
            disabled={purchasing}
          >
            <XCircle size={18} />
            Cancel Purchase
          </button>

          <button
            className="button button-secondary invoice-print-btn no-print"
            onClick={() => window.print()}
            disabled={purchasing}
          >
            <Printer size={18} />
            Print Invoice
          </button>

          <button
            className="button button-primary invoice-confirm-btn"
            onClick={handleConfirm}
            disabled={purchasing}
          >
            <CheckCircle size={18} />
            {purchasing ? 'Processing...' : 'Confirm Purchase'}
          </button>
        </div>

        <p className="invoice-footer-note">
          By confirming, you agree to the dealership's purchase terms. This invoice will be
          finalized upon confirmation. Cancellation returns you to the catalog without any charge.
        </p>
      </div>

      {/* Back link */}
      <button className="billing-back-link no-print" onClick={handleCancel}>
        <ArrowLeft size={14} />
        Back to Fleet
      </button>
    </div>
  );
}

export default BillingPage;
