import React, { useState } from 'react';
import api from '../lib/api';
import { AxiosError } from 'axios';
import styles from '../styles/CallForm.module.css';

const CallForm = ({ onCallCreated }: { onCallCreated: () => void }) => {
  const [customerName, setCustomerName] = useState<string>('');
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [workflow, setWorkflow] = useState<string>('Support');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    // Validation
    if (customerName.trim().length < 2) {
      setError('Name must be at least 2 characters long');
      setLoading(false);
      return;
    }

    // Simple E.164-like validation (starts with +, followed by 7-15 digits)
    const phoneRegex = /^\+?[1-9]\d{1,14}$/;
    if (!phoneRegex.test(phoneNumber.replace(/\s/g, ''))) {
      setError('Please enter a valid phone number (e.g. +14155550100)');
      setLoading(false);
      return;
    }

    try {
      await api.post('/calls/', {
        customer_name: customerName,
        phone_number: phoneNumber,
        workflow: workflow,
      });
      setCustomerName('');
      setPhoneNumber('');
      onCallCreated();
    } catch (err: unknown) {
      console.error('Failed to create call', err);
      if (err instanceof AxiosError && err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Failed to create call. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.card}>
      <h2>New Call Request</h2>
      {error && <div className={styles.errorMessage}>{error}</div>}
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label>Customer Name</label>
          <input
            type="text"
            value={customerName}
            onChange={(e) => setCustomerName(e.target.value)}
            required
            placeholder="John Doe"
            className={styles.input}
          />
        </div>
        <div className={styles.formGroup}>
          <label>Phone Number</label>
          <input
            type="tel"
            value={phoneNumber}
            onChange={(e) => setPhoneNumber(e.target.value)}
            required
            placeholder="+1 555 0199"
            className={styles.input}
          />
        </div>
        <div className={styles.formGroup}>
          <label>Workflow</label>
          <select
            value={workflow}
            onChange={(e) => setWorkflow(e.target.value)}
            className={`${styles.input} ${styles.select}`}
          >
            <option value="Support">Support</option>
            <option value="Sales">Sales</option>
            <option value="Reminder">Reminder</option>
          </select>
        </div>
        <button type="submit" disabled={loading} className={styles.submitBtn}>
          {loading ? 'Submitting...' : 'Start Call'}
        </button>
      </form>
    </div>
  );
};

export default CallForm;
