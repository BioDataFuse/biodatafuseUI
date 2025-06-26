<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Header Section with Title -->
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
          Graph Visualization and Analysis
        </h1>
        <p class="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
          Connect to GraphDB and manage your graph data.
        </p>
      </div>

      <!-- Main Content -->
      <div class="mt-12 bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-800 px-6 py-4">
          <h2 class="text-xl font-semibold text-white">GraphDB Connection</h2>
        </div>

        <div class="p-6">
          <!-- Connection Type Selection -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Connection Type</label>
            <div class="flex space-x-4">
              <label class="flex items-center">
                <input
                  type="radio"
                  v-model="connectionType"
                  value="local"
                  class="mr-2"
                />
                <span>Local GraphDB (localhost:7200)</span>
              </label>
              <label class="flex items-center">
                <input
                  type="radio"
                  v-model="connectionType"
                  value="remote"
                  class="mr-2"
                />
                <span>Remote GraphDB</span>
              </label>
            </div>
          </div>

          <!-- Connection Configuration -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <!-- Base URL -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Base URL</label>
              <input
                type="text"
                v-model="baseUrl"
                :disabled="connectionType === 'local'"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:bg-gray-100"
                placeholder="http://localhost:7200"
              />
            </div>

            <!-- Repository Name -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Repository Name</label>
              <input
                type="text"
                v-model="repositoryName"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="biodatafuse"
              />
            </div>

            <!-- Username -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Username (optional)</label>
              <input
                type="text"
                v-model="username"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="admin"
              />
            </div>

            <!-- Password -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Password (optional)</label>
              <input
                type="password"
                v-model="password"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="password"
              />
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex flex-wrap gap-4 mb-6">
            <button
              @click="testConnection"
              :disabled="loading"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-50"
            >
              Test Connection
            </button>

            <button
              @click="listRepositories"
              :disabled="loading"
              class="inline-flex items-center px-4 py-2 bg-green-600 text-white font-semibold rounded-lg shadow hover:bg-green-500 focus:outline-none focus:ring-2 focus:ring-green-400 disabled:opacity-50"
            >
              List Repositories
            </button>

            <button
              @click="createRepository"
              :disabled="loading"
              class="inline-flex items-center px-4 py-2 bg-yellow-600 text-white font-semibold rounded-lg shadow hover:bg-yellow-500 focus:outline-none focus:ring-2 focus:ring-yellow-400 disabled:opacity-50"
            >
              Create Repository
            </button>

            <button
              @click="uploadGraph"
              :disabled="loading || !repositoryName"
              class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400 disabled:opacity-50"
            >
              Upload Graph Data
            </button>
          </div>

          <!-- Status Messages -->
          <div v-if="loading" class="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
            <div class="flex items-center">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-500 mr-3"></div>
              <span class="text-blue-700">{{ loadingMessage }}</span>
            </div>
          </div>

          <div v-if="statusMessage" class="mb-4 p-4 bg-green-50 border border-green-200 rounded-md">
            <p class="text-green-700">{{ statusMessage }}</p>
          </div>

          <div v-if="errorMessage" class="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
            <p class="text-red-700">{{ errorMessage }}</p>
          </div>

          <!-- Repository List -->
          <div v-if="repositories.length > 0" class="mt-6">
            <h3 class="text-lg font-medium text-gray-900 mb-4">Available Repositories</h3>
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Readable</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white divide-y divide-gray-200">
                  <tr v-for="repo in repositories" :key="repo.id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ repo.id }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ repo.title }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ repo.type }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ repo.readable ? 'Yes' : 'No' }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      <button
                        @click="selectRepository(repo.id)"
                        class="text-indigo-600 hover:text-indigo-900 mr-3"
                      >
                        Select
                      </button>
                      <button
                        @click="queryRepository(repo.id)"
                        class="text-green-600 hover:text-green-900"
                      >
                        Query
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import axios from 'axios'

// Reactive data
const connectionType = ref('local')
const baseUrl = ref('http://localhost:7200')
const repositoryName = ref('biodatafuse')
const username = ref('')
const password = ref('')
const loading = ref(false)
const loadingMessage = ref('')
const statusMessage = ref('')
const errorMessage = ref('')
const repositories = ref([])

// Watch connection type changes
watch(connectionType, (newType) => {
  if (newType === 'local') {
    baseUrl.value = 'http://localhost:7200'
  } else {
    baseUrl.value = ''
  }
  clearMessages()
})

// Helper functions
const clearMessages = () => {
  statusMessage.value = ''
  errorMessage.value = ''
}

const setLoading = (isLoading, message = '') => {
  loading.value = isLoading
  loadingMessage.value = message
}

// API functions
const testConnection = async () => {
  clearMessages()
  setLoading(true, 'Testing connection...')
  
  try {
    const response = await axios.post('/api/graphdb/test-connection', {
      baseUrl: baseUrl.value,
      username: username.value || null,
      password: password.value || null
    })
    statusMessage.value = response.data.message
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to connect to GraphDB'
  } finally {
    setLoading(false)
  }
}

const listRepositories = async () => {
  clearMessages()
  setLoading(true, 'Fetching repositories...')
  
  try {
    const response = await axios.post('/api/graphdb/list-repositories', {
      baseUrl: baseUrl.value,
      username: username.value || null,
      password: password.value || null
    })
    repositories.value = response.data.repositories
    statusMessage.value = `Found ${repositories.value.length} repositories`
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to list repositories'
    repositories.value = []
  } finally {
    setLoading(false)
  }
}

const createRepository = async () => {
  if (!repositoryName.value.trim()) {
    errorMessage.value = 'Repository name is required'
    return
  }
  
  clearMessages()
  setLoading(true, `Creating repository: ${repositoryName.value}`)
  
  try {
    const response = await axios.post('/api/graphdb/create-repository', {
      baseUrl: baseUrl.value,
      repositoryName: repositoryName.value,
      username: username.value || null,
      password: password.value || null
    })
    statusMessage.value = response.data.message
    // Refresh repository list
    await listRepositories()
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to create repository'
  } finally {
    setLoading(false)
  }
}

const uploadGraph = async () => {
  clearMessages()
  setLoading(true, 'Uploading graph data...')
  
  try {
    const response = await axios.post('/api/graphdb/upload-graph', {
      baseUrl: baseUrl.value,
      repositoryId: repositoryName.value,
      username: username.value || null,
      password: password.value || null
    })
    statusMessage.value = response.data.message
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to upload graph data'
  } finally {
    setLoading(false)
  }
}

const selectRepository = (repoId) => {
  repositoryName.value = repoId
  statusMessage.value = `Selected repository: ${repoId}`
}

const queryRepository = async (repoId) => {
  clearMessages()
  setLoading(true, `Querying repository: ${repoId}`)
  
  try {
    const response = await axios.post('/api/graphdb/query', {
      baseUrl: baseUrl.value,
      repositoryName: repoId,
      username: username.value || null,
      password: password.value || null,
      query: 'SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10'
    })
    statusMessage.value = `Query executed. Results: ${JSON.stringify(response.data.results).substring(0, 100)}...`
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to query repository'
  } finally {
    setLoading(false)
  }
}
</script>