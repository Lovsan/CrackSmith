import api from './api';

export const authService = {
  register: async (username, email, password, pin) => {
    const response = await api.post('/auth/register', {
      username,
      email,
      password,
      pin,
    });
    return response.data;
  },

  login: async (username, password, pin) => {
    const response = await api.post('/auth/login', {
      username,
      password,
      pin,
    });
    return response.data;
  },

  getCurrentUser: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },

  setPin: async (pin, currentPin) => {
    const response = await api.post('/auth/set-pin', {
      pin,
      current_pin: currentPin,
    });
    return response.data;
  },

  trackInstallation: async (deviceId, platform, version) => {
    const response = await api.post('/auth/installation', {
      device_id: deviceId,
      platform,
      version,
    });
    return response.data;
  },
};

export const jobService = {
  createJob: async (hashValue, hashType) => {
    const response = await api.post('/jobs/', {
      hash_value: hashValue,
      hash_type: hashType,
    });
    return response.data;
  },

  getJobs: async (status, page = 1, perPage = 20) => {
    const params = { page, per_page: perPage };
    if (status) params.status = status;
    
    const response = await api.get('/jobs/', { params });
    return response.data;
  },

  getJob: async (jobId) => {
    const response = await api.get(`/jobs/${jobId}`);
    return response.data;
  },

  deleteJob: async (jobId) => {
    const response = await api.delete(`/jobs/${jobId}`);
    return response.data;
  },
};

export const statsService = {
  getUserStats: async () => {
    const response = await api.get('/stats/user');
    return response.data;
  },

  getDashboardStats: async () => {
    const response = await api.get('/stats/dashboard');
    return response.data;
  },
};

export const adminService = {
  getAdminStats: async () => {
    const response = await api.get('/admin/stats');
    return response.data;
  },

  getUsers: async (page = 1, perPage = 20) => {
    const response = await api.get('/admin/users', {
      params: { page, per_page: perPage },
    });
    return response.data;
  },

  upgradeUser: async (userId) => {
    const response = await api.post(`/admin/users/${userId}/upgrade`);
    return response.data;
  },

  makeAdmin: async (userId, adminPin) => {
    const response = await api.post(`/admin/users/${userId}/admin`, {
      admin_pin: adminPin,
    });
    return response.data;
  },

  getInstallations: async (page = 1, perPage = 20) => {
    const response = await api.get('/admin/installations', {
      params: { page, per_page: perPage },
    });
    return response.data;
  },

  getAllJobs: async (status, page = 1, perPage = 20) => {
    const params = { page, per_page: perPage };
    if (status) params.status = status;
    
    const response = await api.get('/admin/jobs', { params });
    return response.data;
  },

  getSettings: async () => {
    const response = await api.get('/admin/settings');
    return response.data;
  },

  updateSettings: async (settings) => {
    const response = await api.post('/admin/settings', settings);
    return response.data;
  },
};
