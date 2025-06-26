<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Header Section with Title -->
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
          Graph Visualization and Analysis
        </h1>
        <p class="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
          View and manage data visualization and analysis.
        </p>
      </div>

      <!-- Tab Buttons with Sticky Blue Header -->
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
      <div class="min-h-screen bg-white p-8">
        <div class="max-w-4xl mx-auto text-center">
          <p class="text-lg font-bold text-gray-600 mb-6">
            <strong>Note:</strong> Ensure Cytoscape is open. Click the button below to load your graph.
          </p>

          <button
            @click="loadCytoscapeGraph"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          >
            Load your graph in Cytoscape
          </button>

          <p v-if="statusMessage" class="mt-6 text-lg text-green-600">{{ statusMessage }}</p>
          <p v-if="errorMessage" class="mt-6 text-lg text-red-600">{{ errorMessage }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const statusMessage = ref('')
const errorMessage = ref('')
const identifierSetId = localStorage.getItem('currentIdentifierSetId')

const loadCytoscapeGraph = async () => {
  statusMessage.value = ''
  errorMessage.value = ''
  if (!identifierSetId) {
    errorMessage.value = 'No identifier set selected.'
    return
  }
  try {
    const response = await axios.post(`/api/visualize&analysis/cytoscape/${identifierSetId}`)
    statusMessage.value = response.data.message
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to connect to Cytoscape.'
  }
}

</script>


