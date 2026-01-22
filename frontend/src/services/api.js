import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const styleGuideAPI = {
  // Query the style guide
  query: async (query, sessionId, recaptchaToken) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/bot/query`, {
        query,
        session_id: sessionId,
        recaptcha_token: recaptchaToken
      });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },

  // Health check
  checkHealth: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/bot/health`);
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  // Delete session 
  deleteSession: async (sessionId) => {
    try {
      const response = await axios.delete(`${API_BASE_URL}/bot/session/${sessionId}`);
      return response.data;
    } catch (error) {
      console.error('Delete session error:', error);
      throw error;
    }
  }
};