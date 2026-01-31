import React from 'react';
import useSWR from 'swr';
import api from '../lib/api';
import styles from '../styles/CallList.module.css';

const fetcher = (url: string) => api.get(url).then((res) => res.data);

interface Call {
  id: string;
  customer_name: string;
  phone_number: string;
  workflow: string;
  status: string;
  created_at: string;
}

const CallList = ({ refreshTrigger }: { refreshTrigger: number }) => {
  const { data, error, mutate, isValidating } = useSWR<Call[]>('/calls/', fetcher, {
    refreshInterval: 2000,
  });

  React.useEffect(() => {
    mutate();
  }, [refreshTrigger, mutate]);

  if (error) return (
    <div className={`${styles.card} ${styles.errorState}`}>
      <p>Failed to load calls</p>
    </div>
  );

  if (!data) return (
    <div className={`${styles.card} ${styles.loadingState}`}>
      <p>Loading call history...</p>
    </div>
  );

  const getStatusClass = (status: string) => {
    switch (status.toLowerCase()) {
      case 'pending': return styles.statusPending;
      case 'initiated': return styles.statusInitiated;
      case 'completed': return styles.statusCompleted;
      case 'failed': return styles.statusFailed;
      default: return '';
    }
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <h2>Call History</h2>
        <button onClick={() => mutate()} className={styles.refreshBtn}>
          <svg
            className={isValidating ? styles.spin : ''}
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <polyline points="23 4 23 10 17 10"></polyline>
            <polyline points="1 20 1 14 7 14"></polyline>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
          </svg>
          Refresh
        </button>
      </div>
      <div className={styles.tableContainer}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Customer</th>
              <th>Phone</th>
              <th>Workflow</th>
              <th>Status</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {data.map((call) => (
              <tr key={call.id}>
                <td>
                  <div className={styles.customerName}>{call.customer_name}</div>
                </td>
                <td className={styles.phone}>{call.phone_number}</td>
                <td>
                  <span className={styles.workflowBadge}>{call.workflow}</span>
                </td>
                <td>
                  <span className={`${styles.status} ${getStatusClass(call.status)}`}>
                    {call.status}
                  </span>
                </td>
                <td className={styles.time}>
                  {new Date(call.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </td>
              </tr>
            ))}
            {data.length === 0 && (
              <tr>
                <td colSpan={5} className={styles.emptyState}>
                  No calls recorded yet
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CallList;
