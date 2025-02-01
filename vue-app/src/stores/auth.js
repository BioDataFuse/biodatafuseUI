import { defineStore } from 'pinia'
import axios from 'axios'

// Configure axios defaults
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
axios.defaults.withCredentials = true

// Create axios instance with interceptors
const api = axios.create()

// Add request interceptor to include token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401 && error.config.url !== '/api/auth/login') {
      // Clear auth state on 401 errors (except for login attempts)
      const auth = useAuthStore()
      auth.clearAuth()
    }
    return Promise.reject(error)
  }
)

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    loading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    userProfile: (state) => state.user,
    getError: (state) => state.error,
    isLoading: (state) => state.loading
  },
  
  actions: {
    setLoading(status) {
      this.loading = status
    },

    setError(error) {
      this.error = error
    },

    clearError() {
      this.error = null
    },

    clearAuth() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    },

    async login(email, password) {
      this.setLoading(true)
      this.clearError()
      try {
        const res = await api.post('/api/auth/login', { email, password })
        this.token = res.data.token
        this.user = res.data.user
        localStorage.setItem('token', this.token)
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        return this.user
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Login failed'
        this.setError(errorMessage)
        throw new Error(errorMessage)
      } finally {
        this.setLoading(false)
      }
    },

    async register(userData) {
      this.setLoading(true)
      this.clearError()
      try {
        const res = await api.post('/api/auth/register', userData)
        this.token = res.data.token
        this.user = res.data.user
        localStorage.setItem('token', this.token)
        api.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        return this.user
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Registration failed'
        this.setError(errorMessage)
        throw new Error(errorMessage)
      } finally {
        this.setLoading(false)
      }
    },

    async logout() {
      this.setLoading(true)
      try {
        await api.post('/api/auth/logout')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.clearAuth()
        this.setLoading(false)
      }
    },

    async fetchUserProfile() {
      this.setLoading(true)
      this.clearError()
      try {
        const res = await api.get('/api/auth/me')
        this.user = res.data
        return this.user
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Failed to fetch profile'
        this.setError(errorMessage)
        throw new Error(errorMessage)
      } finally {
        this.setLoading(false)
      }
    },

    async updateProfile(profileData) {
      this.setLoading(true)
      this.clearError()
      try {
        const res = await api.put('/api/auth/profile', profileData)
        this.user = res.data
        return this.user
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Profile update failed'
        this.setError(errorMessage)
        throw new Error(errorMessage)
      } finally {
        this.setLoading(false)
      }
    },

    async updatePassword(passwordData) {
      this.setLoading(true)
      this.clearError()
      try {
        await api.put('/api/auth/password', passwordData)
        return true
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Password update failed'
        this.setError(errorMessage)
        throw new Error(errorMessage)
      } finally {
        this.setLoading(false)
      }
    },

    async regenerateApiKey() {
      this.setLoading(true)
      this.clearError()
      try {
        const res = await api.post('/api/auth/regenerate-api-key')
        this.user = res.data
        return this.user
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Failed to regenerate API key'
        this.setError(errorMessage)
        throw new Error(errorMessage)
      } finally {
        this.setLoading(false)
      }
    }
  }
})
