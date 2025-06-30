import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
  appType: 'spa',
  plugins: [vue()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://backend:8000',
        changeOrigin: true
      },
      '/api-docs': {
        target: process.env.VITE_API_URL || 'http://backend:8000',
        changeOrigin: true
      },
      '/docs': {
        target: process.env.VITE_API_URL || 'http://backend:8000',
        changeOrigin: true
      }
    },
    historyApiFallback: true
  }
})