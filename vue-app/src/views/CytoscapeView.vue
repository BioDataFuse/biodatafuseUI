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
        <div class="p-6 text-gray-700 space-y-6">
          <!-- Graph Name Input -->
          <div class="mb-6">
            <label class="block text-gray-700 font-medium mb-2">Custom Graph Name</label>
            <input
              v-model="graphName"
              @input="handleInput"
              type="text"
              placeholder="e.g. MyCytoscapeGraph"
              class="w-full border border-gray-300 rounded px-3 py-2"
            />
          </div>

          <!-- Status Messages -->
          <p v-if="statusMessage" class="text-lg text-green-600">{{ statusMessage }}</p>
          <p v-if="errorMessage" class="text-lg text-red-600">{{ errorMessage }}</p>

          <!-- Instructions for Remote Web Server and Local Cytoscape -->
          <div class="mt-10 border-t pt-8">
            <button @click="toggleRemoteInstructions" class="text-indigo-600 font-medium hover:underline">
              {{ showRemoteInstructions ? 'Instructions for loading the graph into Cytoscape on Local Machine (hide) ▲' : 'Instructions for loading the graph into Cytoscape on Local Machine (show) ▼' }}
            </button>
            <div v-if="showRemoteInstructions">
              <p class="text-lg font-semibold text-gray-800 mb-4">
              </p>
              <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
                <li>Ensure Cytoscape Desktop is installed and running on your local machine.</li>
                <li>Start the local Cytoscape bridge by running <code>python cytoscape_bridge.py</code> in a terminal on your local machine.</li>
                <div class="mt-4">
                  <!-- Download Link for cytoscape_bridge.py -->
                  <a
                    href="https://github.com/BioDataFuse/biodatafuseUI/blob/main/backend/app/static/cytoscape_bridge.py"
                    target="_blank"
                    class="inline-flex items-center border border-blue-500 px-4 py-2 text-sm font-semibold text-blue-700 rounded-lg hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-blue-400"
                    download
                  >
                    <svg class="w-4 h-4 mr-2 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                    </svg>
                    Save Cytoscape Bridge (cytoscape_bridge.py)
                  </a>
                </div>
                <li>Ensure the REST API is enabled in Cytoscape (default setting).</li>
                <li>Enter the graph name and click <strong>"Load your graph into Cytoscape"</strong>.</li>
                <!-- Load Graph into Cytoscape (Button) -->
                <button
                  @click="loadCytoscapeGraph"
                  :disabled="loading"
                  class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                >
                  <span v-if="loading" class="animate-spin mr-2">🔄</span>
                  <span>{{ loading ? 'Loading...' : 'Load your graph into Cytoscape' }}</span>
                </button>
                <li>The graph will be sent to your local Cytoscape instance via the local Cytoscape bridge.</li>
              </ul>

            </div>
          </div>

          <!-- Manual Import Section -->
          <div class="mt-10 border-t pt-8">
            <button @click="toggleManualInstructions" class="text-indigo-600 font-medium hover:underline">
              {{ showManualInstructions ? 'Instructions for manual import (hide) ▲' : 'Instructions for manual import (show) ▼' }}
            </button>
            <div v-if="showManualInstructions">
              <p class="text-lg font-semibold text-gray-800 mb-4">
              </p>
              <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
                <li>Enter the graph name.</li>
                <li>Download the graph JSON and style file using the buttons below.</li>

                <!-- Download Buttons -->
                <div class="flex flex-col md:flex-row items-start md:items-center gap-4">
                  <button
                    @click="downloadGraphJSON"
                    class="inline-flex items-center border border-gray-400 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400"
                  >
                    <svg class="w-4 h-4 mr-2 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                    </svg>
                    Download Graph (JSON)
                  </button>
                  <a
                    href="/api/visualize&analysis/cytoscape/style/download"
                    class="inline-flex items-center border border-green-500 px-4 py-2 text-sm font-semibold text-green-700 rounded-lg hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-green-400"
                    download
                  >
                    <svg class="w-4 h-4 mr-2 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                    </svg>
                    Download Style File
                  </a>
                </div>
                <li>Install and Open Cytoscape Desktop.</li>
                <li>Use <strong>File → Import → Network from File...</strong> to load the graph.</li>
                <li>Use <strong>File → Import → Styles from File...</strong> to import the style.</li>
                <li>After import, go to the <strong>Style panel</strong> and select the style name.</li>
                <li>To organize nodes, go to <strong>Layout → [select layout]</strong> such as "Circular layout".</li>
              </ul>


            </div>
          </div>

          <!-- Instructions for Docker Users -->
          <div class="mt-10 border-t pt-8">
            <button @click="toggleDockerInstructions" class="text-indigo-600 font-medium hover:underline">
              {{ showDockerInstructions ? 'Instructions for running the BioDataFuse UI using Docker (hide) ▲' : 'Instructions for running the BioDataFuse UI using Docker (show) ▼' }}
            </button>
            <div v-if="showDockerInstructions">
              <p class="text-lg font-semibold text-gray-800 mb-4">
              </p>
              <ul class="list-disc list-inside text-gray-700 space-y-1 mb-4">
                <li>Ensure Cytoscape Desktop is installed and running on your local machine.</li>
                <li>Build and run the Docker containers for the BioDataFuse UI (download 
                  <a
                    href="https://github.com/BioDataFuse/biodatafuseUI/blob/main/docker-compose.yaml"
                    target="_blank"
                    class="text-indigo-600 hover:underline"
                  >
                    here
                  </a> 
                  ).
                </li>
                <li>Once the containers are up, go back to the BioDataFuse UI and enter the custom graph name, then click <strong>"Load your graph into Cytoscape"</strong></li>
                <!-- Load Graph into Cytoscape (Button) -->
                <button
                  @click="loadLocalCytoscapeGraph"
                  :disabled="loading"
                  class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                >
                  <span v-if="loading" class="animate-spin mr-2">🔄</span>
                  <span>{{ loading ? 'Loading...' : 'Load your graph into Cytoscape' }}</span>
                </button>
                <li>The graph will be automatically loaded into Cytoscape via the Dockerized app on the same machine.</li>
              </ul>

          
            </div>
          </div>


        </div>


      <!-- Footer Buttons -->
      <div class="flex justify-left items-center bg-white rounded-xl shadow-lg px-6 py-4">
        <br>
        <button
          @click="goBack"
          class="px-4 py-2 border border-indigo-600 text-indigo-600 font-semibold rounded-lg hover:bg-indigo-100"
        >
          ← Select another visualization tool
        </button>
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

const showRemoteInstructions = ref(false)
const showManualInstructions = ref(false)
const showDockerInstructions = ref(false)

const toggleRemoteInstructions = () => {
  showRemoteInstructions.value = !showRemoteInstructions.value
}

const toggleManualInstructions = () => {
  showManualInstructions.value = !showManualInstructions.value
}

const toggleDockerInstructions = () => {
  showDockerInstructions.value = !showDockerInstructions.value
}

const graphName = ref('')
const statusMessage = ref('')
const errorMessage = ref('')
const loading = ref(false)
const cytoscapeResults = ref(null)

const identifierSetId = localStorage.getItem('currentIdentifierSetId')

// Define the URL
const LOCAL_CYTOSCAPE_BRIDGE_URL = 'http://localhost:5001/load_graph_local';

const handleInput = () => {
  if (errorMessage.value.includes('graph name') || errorMessage.value.includes('Identifier set')) {
    errorMessage.value = ''
  }
}

const loadLocalCytoscapeGraph = async () => {
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

  loading.value = true
  try {
    const response = await axios.post(`/api/visualize&analysis/cytoscape/local_to_local/${identifierSetId}`, {
      graph_name: graphName.value.trim()
    })
    statusMessage.value = response.data.message
    errorMessage.value = '' // clear error on success
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to connect to Cytoscape.'
  } finally {
    loading.value = false
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

  loading.value = true
  try {
    statusMessage.value = 'Fetching graph data from server...'
    const backendResponse = await axios.post(`/api/visualize&analysis/cytoscape/${identifierSetId}`, {
      graph_name: graphName.value.trim()
    });

    const { graph_data, network_name } = backendResponse.data;

    if (!graph_data) {
      errorMessage.value = 'Server returned incomplete graph data.';
      loading.value = false;
      return;
    }

    statusMessage.value = 'Sending graph data to local Cytoscape bridge...'
    const localResponse = await axios.post(LOCAL_CYTOSCAPE_BRIDGE_URL, {
      graph_data: graph_data,
      network_name: network_name
    });

    console.log("Sending to local bridge:", {
      graph_data: graph_data,
      network_name: network_name
    })
    if (localResponse.data.success) {
      statusMessage.value = localResponse.data.message;
    } else {
      errorMessage.value = localResponse.data.message || 'Failed to load graph into Cytoscape via local bridge.';
    }

  } catch (error) {
    console.error("Error during Cytoscape graph loading:", error);
    if (error.response) {
      // Error from either backend or local bridge
      errorMessage.value = error.response.data?.detail || error.response.data?.message || 'An unknown error occurred.';
    } else if (error.request) {
      // No response received (e.g., local bridge not running, or network issue to backend)
      if (error.config.url === LOCAL_CYTOSCAPE_BRIDGE_URL) {
          errorMessage.value = `Could not connect to local Cytoscape bridge at ${LOCAL_CYTOSCAPE_BRIDGE_URL}. Please ensure it is running.`;
      } else {
          errorMessage.value = 'Network error or backend server is unreachable.';
      }
    } else {
      // Something else happened in setting up the request
      errorMessage.value = 'Request setup error: ' + error.message;
    }
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  loading.value = true

  if (!identifierSetId) {
    errorMessage.value = 'No identifier set ID found. Please go back and reprocess.'
    loading.value = false
    return
  }

  if (!graphName.value.trim()) {
    errorMessage.value = 'Please provide a graph name to fetch Cytoscape data.'
    loading.value = false
    return
  }

  try {
    const response = await axios.post(`/api/visualize&analysis/cytoscape/download/${identifierSetId}`, {
      graph_name: graphName.value.trim()
    })

    cytoscapeResults.value = response.data
    statusMessage.value = "Cytoscape graph loaded successfully."
    errorMessage.value = '' // clear error on success
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to fetch Cytoscape graph data.'
    console.error("Error loading cytoscapeResults:", error)
  } finally {
    loading.value = false
  }
})

const goBack = () => {
  router.push('/visualize&analysis')
}

const downloadGraphJSON = async () => {
  if (!identifierSetId || !graphName.value.trim()) {
    errorMessage.value = 'Graph name is missing.'
    return
  }

  try {
    const response = await axios.post(`/api/visualize&analysis/cytoscape/download/${identifierSetId}`, {
      graph_name: graphName.value.trim()
    })

    const graphData = response.data?.cytoscape_graph
    if (!graphData) {
      throw new Error('No cytoscape_graph found in response.')
    }

    const json = JSON.stringify(graphData, null, 2)
    const blob = new Blob([json], { type: 'application/json' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `${graphName.value.trim()}.json`
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(link.href)

    statusMessage.value = 'Cytoscape graph JSON download started.'
    errorMessage.value = '' // clear any previous error
  } catch (err) {
    console.error('Download error:', err)
    errorMessage.value = err.response?.data?.detail || err.message || 'Failed to download Cytoscape JSON.'
  }
}
</script>
