import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { api } from "@/services/api";
import type { User, LoginCredentials, RegisterCredentials } from "@/types";

export const useAuthStore = defineStore("auth", () => {
  const user = ref<User | null>(
    localStorage.getItem("user")
      ? JSON.parse(localStorage.getItem("user")!)
      : null,
  );
  const token = ref<string | null>(localStorage.getItem("token"));
  const loading = ref(false);
  const error = ref<string | null>(null);

  const isAuthenticated = computed(() => !!token.value && !!user.value);

  const login = async (credentials: LoginCredentials) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await api.post("/auth/login", credentials);
      const data = response.data;

      user.value = {
        id: data.id,
        email: data.email,
        full_name: data.full_name,
      };
      token.value = data.access_token;

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(user.value));

      return data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Login failed";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const register = async (credentials: RegisterCredentials) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await api.post("/auth/register", credentials);
      const data = response.data;

      user.value = {
        id: data.id,
        email: data.email,
        full_name: data.full_name,
      };
      token.value = data.access_token;

      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(user.value));

      return data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || "Registration failed";
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const logout = async () => {
    user.value = null;
    token.value = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  const initializeAuth = () => {
    const storedToken = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");

    if (storedToken && storedUser) {
      token.value = storedToken;
      user.value = JSON.parse(storedUser);
    }
  };

  const clearError = () => {
    error.value = null;
  };

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    initializeAuth,
    clearError,
  };
});
