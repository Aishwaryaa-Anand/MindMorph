import axios from 'axios';

const API_URL = 'http://localhost:5000/api/questionnaire';

export const questionnaireService = {
  // Get all questions
  getQuestions: async () => {
    const response = await axios.get(`${API_URL}/questions`);
    return response.data;
  },

  // Submit answers and get prediction
  predict: async (answers) => {
    const response = await axios.post(`${API_URL}/predict`, { answers });
    return response.data;
  },

  // Get latest result
  getLatestResult: async () => {
    const response = await axios.get(`${API_URL}/results`);
    return response.data;
  },

  // Get specific result by ID
  getResultById: async (id) => {
    const response = await axios.get(`${API_URL}/result/${id}`);
    return response.data;
  },

  // Get history
  getHistory: async () => {
    const response = await axios.get(`${API_URL}/history`);
    return response.data;
  },

  // Get insights for any MBTI type
  getInsights: async (mbtiType) => {
    const response = await axios.get(`${API_URL}/insights/${mbtiType}`);
    return response.data;
  }
};