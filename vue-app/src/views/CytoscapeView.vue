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

      <!-- Instructions -->
      <div class="mt-12 bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-800 px-6 py-4">
          <h2 class="text-xl font-semibold text-white">Visualization in Cytoscape</h2>
        </div>
        <div class="p-6 text-gray-700">
          <p class="text-xl text-gray-600 mb-6">
            <strong>Instructions:</strong><br><br>
            • Ensure <strong>Cytoscape Desktop</strong> is installed and running on your local machine.<br>
            • The <strong>REST API</strong> must be enabled (default setting).<br>
            • Complete the query building step before visualization.<br>
            • A graph with no edges will result in an error.
          </p>

          <!-- Cytoscape Status Check -->
          <div class="mb-6 p-4 rounded-lg" :class="cytoscapeStatus.class">
            <div class="flex items-center">
              <span class="mr-2">{{ cytoscapeStatus.icon }}</span>
              <span class="font-medium">{{ cytoscapeStatus.message }}</span>
              <button 
                @click="checkCytoscapeConnection" 
                class="ml-auto px-3 py-1 text-sm bg-white bg-opacity-20 rounded hover:bg-opacity-30"
                :disabled="checkingConnection"
              >
                {{ checkingConnection ? 'Checking...' : 'Recheck' }}
              </button>
            </div>
          </div>

          <!-- Graph Name Input -->
          <div class="mb-6">
            <label class="block text-gray-700 font-medium mb-2">Custom Graph Name</label>
            <input
              v-model="graphName"
              type="text"
              placeholder="e.g. MyCytoscapeGraph"
              class="w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <!-- Status Messages -->
          <p v-if="statusMessage" class="mt-6 text-lg text-green-600">{{ statusMessage }}</p>
          <p v-if="errorMessage" class="mt-6 text-lg text-red-600">{{ errorMessage }}</p>

          <!-- Footer Buttons -->
          <div class="mt-8 flex justify-between items-center bg-white rounded-b-xl shadow-lg px-6 py-4">
            <button
              @click="goBack"
              class="px-4 py-2 border border-indigo-600 text-indigo-600 font-semibold rounded-lg hover:bg-indigo-100"
            >
              ← Select another visualization tool
            </button>

            <button
              @click="loadCytoscapeGraph"
              :disabled="loading || !cytoscapeConnected"
              class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <span v-if="loading" class="animate-spin mr-2">🔄</span>
              <span>{{ getLoadButtonText() }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const statusMessage = ref('')
const errorMessage = ref('')
const loading = ref(false)
const checkingConnection = ref(false)
const cytoscapeConnected = ref(false)
const graphName = ref('')
const identifierSetId = localStorage.getItem('currentIdentifierSetId')

const cytoscapeStatus = ref({
  message: 'Checking Cytoscape connection...',
  icon: '🔄',
  class: 'bg-yellow-100 text-yellow-800'
})

const checkCytoscapeConnection = async () => {
  checkingConnection.value = true
  try {
    const response = await fetch('http://localhost:1234/v1/status', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    
    if (response.ok) {
      cytoscapeConnected.value = true
      cytoscapeStatus.value = {
        message: 'Cytoscape is running and ready!',
        icon: '✅',
        class: 'bg-green-100 text-green-800'
      }
    } else {
      throw new Error('Cytoscape not responding')
    }
  } catch (error) {
    cytoscapeConnected.value = false
    cytoscapeStatus.value = {
      message: 'Cytoscape not detected. Please start Cytoscape Desktop.',
      icon: '❌',
      class: 'bg-red-100 text-red-800'
    }
  } finally {
    checkingConnection.value = false
  }
}

const loadCytoscapeGraph = async () => {
  statusMessage.value = ''
  errorMessage.value = ''

  if (!identifierSetId) {
    errorMessage.value = 'No identifier set selected. Please process your data first.'
    return
  }

  if (!graphName.value.trim()) {
    errorMessage.value = 'Please provide a graph name.'
    return
  }

  if (!cytoscapeConnected.value) {
    errorMessage.value = 'Cytoscape is not running. Please start Cytoscape Desktop and try again.'
    return
  }

  loading.value = true
  
  try {
    // Step 1: Get graph data from your FastAPI server
    statusMessage.value = 'Generating graph data...'
    const response = await axios.post(`/api/visualize&analysis/cytoscape/${identifierSetId}`, {
      graph_name: graphName.value.trim()
    })

    const graphData = response.data.graph_data
    const networkName = response.data.graph_name

    // Step 2: Load graph into local Cytoscape
    statusMessage.value = 'Loading graph into Cytoscape...'
    const cytoscapeResponse = await fetch('http://localhost:1234/v1/networks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...graphData,
        data: {
          ...graphData.data,
          name: networkName
        }
      })
    })

    if (cytoscapeResponse.ok) {
      const result = await cytoscapeResponse.json()
      statusMessage.value = `Graph "${networkName}" loaded successfully into Cytoscape! Network ID: ${result.networkSUID || 'N/A'}`
      
      // Optional: Apply BioDataFuse styling
      await applyBioDataFuseStyle()
      
    } else {
      const errorText = await cytoscapeResponse.text()
      throw new Error(`Failed to load graph into Cytoscape: ${errorText}`)
    }

  } catch (error) {
    console.error('Error loading graph:', error)
    if (error.response?.data?.detail) {
      errorMessage.value = error.response.data.detail
    } else if (error.message) {
      errorMessage.value = error.message
    } else {
      errorMessage.value = 'Failed to load graph. Please check your connection and try again.'
    }
  } finally {
    loading.value = false
  }
}

const applyBioDataFuseStyle = async () => {
  try {
    // Apply the BioDataFuse visual style if available
    await fetch('http://localhost:1234/v1/styles', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: "BioDataFuse_style",
        defaults: [
          {"visualProperty": "NODE_FILL_COLOR", "value": "#FF0000"},
          {"visualProperty": "EDGE_COLOR", "value": "#000000"},
        ],
        mappings: []
      })
    })
  } catch (error) {
    console.warn('Could not apply BioDataFuse style:', error)
  }
}

const getLoadButtonText = () => {
  if (loading.value) return 'Loading...'
  if (!cytoscapeConnected.value) return 'Cytoscape not detected'
  return 'Load your graph into Cytoscape'
}

const goBack = () => {
  router.push('/visualize&analysis')
}

// Check Cytoscape connection when component mounts
onMounted(() => {
  checkCytoscapeConnection()
})
</script>