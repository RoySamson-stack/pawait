import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://192.168.250.52:8000/api';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * @param {string} query - The user's question
 * @returns {Promise<Object>} - The response object
 */
export const sendQuery = async (query) => {
  try {
    const response = await apiClient.post('/qa/query', { query });
    return response.data;
  } catch (error) {
    console.error('API error:', error.response?.data || error.message);
    throw new Error(error.response?.data?.detail || 'Failed to get response from server');
  }
};

/**
 * @returns {Promise<Object>} - The health status
 */
export const checkApiHealth = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw new Error('API health check failed');
  }
};