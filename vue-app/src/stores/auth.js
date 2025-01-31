import { defineStore } from 'pinia'
import axios from 'axios'

axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
axios.defaults.withCredentials = true

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    userProfile: (state) => state.user,
  },
  
  actions: {
    async login(email, password) {
      try {
        const res = await axios.post('/api/auth/login', { email, password })
        this.token = res.data.token
        this.user = res.data.user
        localStorage.setItem('token', this.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        return true
      } catch (error) {
        console.error('Login failed:', error)
        throw error
      }
    },

    async register(userData) {
      try {
        const res = await axios.post('/api/auth/register', userData)
        this.token = res.data.token
        this.user = res.data.user
        localStorage.setItem('token', this.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`
        return true
      } catch (error) {
        console.error('Registration failed:', error)
        throw error
      }
    },

    async logout() {
      try {
        await axios.post('/api/auth/logout')
      } catch (error) {
        console.error('Logout error:', error)
      } finally {
        this.token = null
        this.user = null
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
      }
    },

    async updateProfile(profileData) {
      try {
        const res = await axios.put('/api/auth/profile', profileData)
        this.user = res.data
        return true
      } catch (error) {
        console.error('Profile update failed:', error)
        throw error
      }
    },
  },
})