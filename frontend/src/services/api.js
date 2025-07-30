const API_BASE_URL = 'http://127.0.0.1:8000';

const handleResponse = async (response) => {
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || data.message || 'Something went wrong');
  }
  return data;
};

export const api = {
  async login(credentials) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(credentials),
    });
    return handleResponse(response);
  },

  async register(userData) {
    const response = await fetch(`${API_BASE_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData),
    });
    return handleResponse(response);
  },

  async getCurrentUser() {
    const token = sessionStorage.getItem('authToken');
    if (!token) throw new Error('No token found');

    const response = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  async getAllFileNames() {
    const token = sessionStorage.getItem('authToken');
    const response = await fetch(`${API_BASE_URL}/file/all-file-names`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },

  async searchGraphs({ filename, name, graph_type }) {
    const token = sessionStorage.getItem('authToken');
    const response = await fetch(`${API_BASE_URL}/graph/search`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ filename, name, graph_type }),
    });
    return handleResponse(response);
  },

  async getAllMyGraphs() {
    const token = sessionStorage.getItem('authToken');
    const response = await fetch(`${API_BASE_URL}/graph/mygraphs`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    return handleResponse(response);
  },
}; 