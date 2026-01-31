import axios from 'axios';

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
    headers: {
        'Authorization': `Bearer ${process.env.NEXT_PUBLIC_AUTH_TOKEN || 'super-secret-token-123'}`
    }
});

export default api;
