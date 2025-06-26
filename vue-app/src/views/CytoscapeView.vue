<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
          Graph Visualization and Analysis
        </h1>
        <p class="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
          Load your graph into Cytoscape.
        </p>
      </div>

      <!-- Tab Bar -->
      <div class="mt-12 bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-800 px-6 py-4">
          <div class="flex space-x-8">
            <p
              @click="selectedTab = 'visualization'"
              class="pb-2 text-xl font-medium focus:outline-none"
            >
              <h2 class="text-xl font-semibold text-white">Visualization in Cytoscape</h2>
            </p>
          </div>
        </div>
      </div>

      <!-- Instructions-->
      <div class="from-indigo-600 to-indigo-800 px-6 py-4">
        <div class="mt-1 text-black text-xl">
          <p class="text-xl text-gray-600 mb-6">
            <strong>Instructions:</strong><br>
            <br>
            • Ensure <strong>Cytoscape Desktop</strong> is installed and currently running.<br>
            • Confirm that the <strong>Cytoscape REST API</strong> is enabled (default setting).<br>
            • Complete the data processing and annotations steps before attempting visualization.<br>
            • If your graph contains no edges, you will receive an error and may need to revisit your dataset.
            <br>
          </p>
        </div>
        <!-- Footer Actions -->
        <div class="mt-8 flex justify-between px-6 py-4 bg-white rounded-b-xl shadow-lg">
          <button
            @click="goBack"
            class="px-4 py-2 border border-indigo-600 text-indigo-600 font-semibold rounded-lg hover:bg-indigo-100"
          >
            ← Select another visualization tool
          </button>
          <button
            @click="loadCytoscapeGraph"
            :disabled="loading"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          >
            <span v-if="loading" class="animate-spin mr-2">🔄</span>
            <span>{{ loading ? 'Loading...' : 'Load your graph into Cytoscape' }}</span>
          </button>
        </div>
        <p v-if="statusMessage" class="mt-6 text-lg text-green-600">{{ statusMessage }}</p>
        <p v-if="errorMessage" class="mt-6 text-lg text-red-600">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const statusMessage = ref('')
const errorMessage = ref('')
const loading = ref(false)
const identifierSetId = localStorage.getItem('currentIdentifierSetId')

const loadCytoscapeGraph = async () => {
  statusMessage.value = ''
  errorMessage.value = ''
  if (!identifierSetId) {
    errorMessage.value = 'No identifier set selected. Please process your data first.'
    return
  }

  loading.value = true
  try {
    const response = await axios.post(`/api/visualize&analysis/cytoscape/${identifierSetId}`)
    statusMessage.value = response.data.message
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to connect to Cytoscape.'
  } finally {
    loading.value = false
  }
}
function goBack() {
  router.push('/visualize&analysis')
}
</script>

