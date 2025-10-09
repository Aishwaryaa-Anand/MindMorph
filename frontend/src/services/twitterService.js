import axios from 'axios';

const API_URL = 'http://localhost:5000/api/twitter';

export const twitterService = {
  // Analyze Twitter profile
  analyze: async (username) => {
    const response = await axios.post(`${API_URL}/analyze`, { username });
    return response.data;
  },

  // Get latest Twitter prediction
  getLatestResult: async () => {
    const response = await axios.get(`${API_URL}/results`);
    return response.data;
  },

  // Get specific result by ID
  getResultById: async (id) => {
    const response = await axios.get(`${API_URL}/result/${id}`);
    return response.data;
  },

  // Get prediction history
  getHistory: async () => {
    const response = await axios.get(`${API_URL}/history`);
    return response.data;
  },

  // Get available usernames (public)
  getAvailableUsernames: async () => {
    const response = await axios.get(`${API_URL}/available-usernames`);
    return response.data;
  }
};