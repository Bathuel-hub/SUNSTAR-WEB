import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Add request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// API functions
export const api = {
  // Company Information
  getCompanyInfo: async () => {
    const response = await apiClient.get('/company-info');
    return response.data;
  },

  // Products
  getProductCategories: async () => {
    const response = await apiClient.get('/products/categories');
    return response.data;
  },

  getSampleProducts: async (categoryId) => {
    const response = await apiClient.get(`/products/sample/${categoryId}`);
    return response.data;
  },

  getProductsByCategory: async (categoryId) => {
    const response = await apiClient.get(`/products/category/${categoryId}`);
    return response.data;
  },

  // Contact
  submitContactInquiry: async (inquiryData) => {
    const response = await apiClient.post('/contact/inquiry', inquiryData);
    return response.data;
  },

  // Testimonials
  getTestimonials: async (featuredOnly = true) => {
    const response = await apiClient.get('/testimonials', {
      params: { featured_only: featuredOnly }
    });
    return response.data;
  },

  // Why Choose Us
  getAdvantages: async () => {
    const response = await apiClient.get('/advantages');
    return response.data;
  },

  // Statistics
  getStats: async () => {
    const response = await apiClient.get('/stats');
    return response.data;
  },

  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/');
    return response.data;
  }
};

export default api;