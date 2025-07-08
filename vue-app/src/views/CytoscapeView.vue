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
            • Ensure <strong>Cytoscape Desktop</strong> is installed and running.<br>
            • The <strong>REST API</strong> must be enabled (default setting).<br>
            • Complete the query building step before visualization.<br>
            • A graph with no edges will result in an error.
          </p>

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
            <!-- Download Cytoscape graph (JSON) -->
            <button 
              @click="downloadGraphJSON" 
              class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400">
              <svg class="w-4 h-4 mr-2 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
              </svg>
              Download Cytoscape graph (JSON)
            </button>

            <!-- Download Cytoscape style -->
            <a
              href="/api/visualize&analysis/cytoscape/style/download"
              class="inline-flex items-center border-2 border-dashed border-green-600 px-4 py-2 text-sm font-semibold text-green-700 rounded-lg hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-green-400"
              download
            >
              <svg class="w-4 h-4 mr-2 text-green-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
              </svg>
              Download Cytoscape style
            </a>

            <button
              @click="loadCytoscapeGraph"
              :disabled="loading"
              class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400"
            >
              <span v-if="loading" class="animate-spin mr-2">🔄</span>
              <span>{{ loading ? 'Loading...' : 'Load your graph into Cytoscape' }}</span>
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
const cytoscapeResults = ref(null)

const loading = ref(false)
const graphName = ref('')
const identifierSetId = localStorage.getItem('currentIdentifierSetId')

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
    const response = await axios.post(`/api/visualize&analysis/cytoscape/${identifierSetId}`, {
      graph_name: graphName.value.trim()
    })
    statusMessage.value = response.data.message
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to connect to Cytoscape.'
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
    errorMessage.value = 'Identifier set ID or graph name is missing.';
    return;
  }

  try {
    const response = await axios.post(`/api/visualize&analysis/cytoscape/download/${identifierSetId}`, {
      graph_name: graphName.value.trim()
    });

    const graphData = response.data?.cytoscape_graph;
    if (!graphData) {
      throw new Error('No cytoscape_graph found in response.');
    }

    const json = JSON.stringify(graphData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${graphName.value.trim()}.json`;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(link.href);

    statusMessage.value = 'Cytoscape graph JSON download started.';
  } catch (err) {
    console.error('Download error:', err);
    errorMessage.value = err.response?.data?.detail || err.message || 'Failed to download Cytoscape JSON.';
  }
};


</script>
