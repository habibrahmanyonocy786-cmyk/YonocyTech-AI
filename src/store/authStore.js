import { create } from 'zustand';

const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,
  token: localStorage.getItem('token') || null,
  loading: false,
  error: null,

  signup: async (userData) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message);
      
      localStorage.setItem('token', data.token);
      set({
        user: data.user,
        isAuthenticated: true,
        token: data.token,
        loading: false,
      });
      return data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  login: async (credentials) => {
    set({ loading: true, error: null });
    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message);
      
      localStorage.setItem('token', data.token);
      set({
        user: data.user,
        isAuthenticated: true,
        token: data.token,
        loading: false,
      });
      return data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
    set({ user: null, isAuthenticated: false, token: null });
  },

  clearError: () => set({ error: null }),
}));

export default useAuthStore;
export { useAuthStore };
