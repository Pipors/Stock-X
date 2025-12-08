// API Service Module - Handles all API communication
// static/js/api.js

const ApiService = {
  baseUrl: '',

  async fetch(endpoint) {
    try {
      const response = await fetch(`${this.baseUrl}/api/${endpoint}`);
      const result = await response.json();
      if (!result.success) throw new Error(result.error || 'API request failed');
      return result.data;
    } catch (error) {
      console.error(`❌ API Error (${endpoint}):`, error);
      throw error;
    }
  },

  async getDashboardData(refresh = false) {
    return this.fetch(`dashboard${refresh ? '?refresh=true' : ''}`);
  },

  async getKpiDetails(kpiId) {
    return this.fetch(`kpi/${kpiId}`);
  }
};

// Export for use in other modules
window.ApiService = ApiService;
