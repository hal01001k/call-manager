import type { NextPage } from 'next';
import Head from 'next/head';
import { useState } from 'react';
import CallForm from '../components/CallForm';
import CallList from '../components/CallList';
import styles from '../styles/Home.module.css';

const Home: NextPage = () => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleCallCreated = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Call Manager</title>
        <meta name="description" content="Manage your automated calls" />
        <link rel="icon" href="/favicon.ico" />
        {/* Google Fonts */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
      </Head>

      <main className={styles.main}>
        <div className={styles.headerSection}>
          <h1 className={styles.title}>Call Manager</h1>
          <p className={styles.subtitle}>Automated Voice Workflow System</p>
        </div>

        <div className={styles.grid}>
          <div className={`${styles.column} ${styles.formColumn}`}>
            <CallForm onCallCreated={handleCallCreated} />
          </div>
          <div className={`${styles.column} ${styles.listColumn}`}>
            <CallList refreshTrigger={refreshTrigger} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
