import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

export const propertyService = {
  getAll: async () => {
    const response = await api.get("/properties");
    return response.data;
  },
  getById: async (id: number) => {
    const response = await api.get(`/properties/${id}`);
    return response.data;
  },
  create: async (data: any) => {
    const response = await api.post("/properties", data);
    return response.data;
  },
  update: async (id: number, data: any) => {
    const response = await api.put(`/properties/${id}`, data);
    return response.data;
  },
  delete: async (id: number) => {
    const response = await api.delete(`/properties/${id}`);
    return response.data;
  },
  getAnalysis: async () => {
    const response = await api.post("/properties/analyze");
    return response.data;
  }
};

export default api;
