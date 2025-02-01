<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:px-6">
          <h2 class="text-xl font-bold text-gray-900">Network Visualization</h2>
          <p class="mt-1 text-sm text-gray-500">
            Explore and analyze your integrated biological network
          </p>
        </div>
      </div>

      <!-- Main Content -->
      <div class="grid grid-cols-4 gap-6">
        <!-- Left Sidebar - Controls -->
        <div class="col-span-1 space-y-6">
          <!-- Network Stats -->
          <NetworkStats :stats="networkStats" />

          <!-- Network Filters -->
          <NetworkFilters 
            :dataSources="dataSources"
            :nodeTypes="nodeTypes"
            :nodeColors="nodeColors"
            @update="handleFilterUpdate"
          />

          <!-- Network Toolbar -->
          <NetworkToolbar 
            @layout-change="handleLayoutChange"
            @zoom="handleZoom"
            @export="handleExport"
          />
        </div>

        <!-- Main Network View -->
        <div class="col-span-3">
          <!-- Loading State -->
          <div v-if="loading" class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center justify-center h-96">
              <div class="flex flex-col items-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500"></div>
                <p class="mt-4 text-sm text-gray-500">Loading network data...</p>
              </div>
            </div>
          </div>

          <!-- Error State -->
          <div v-else-if="error" class="bg-white rounded-lg shadow p-6">
            <div class="rounded-md bg-red-50 p-4">
              <div class="flex">
                <ExclamationCircleIcon class="h-5 w-5 text-red-400" />
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-red-800">{{ error }}</h3>
                  <div class="mt-2">
                    <button 
                      @click="retryLoading"
                      class="text-sm text-red-600 hover:text-red-500"
                    >
                      Try again
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Network View -->
          <div v-else class="bg-white rounded-lg shadow">
            <div ref="networkContainer" class="h-[800px] relative" id="cy">
              <!-- No Data State -->
              <div v-if="!hasData" class="absolute inset-0 flex items-center justify-center">
                <div class="text-center">
                  <NoSymbolIcon class="mx-auto h-12 w-12 text-gray-400" />
                  <h3 class="mt-2 text-sm font-medium text-gray-900">No network data</h3>
                  <p class="mt-1 text-sm text-gray-500">
                    Return to the query page to build your network.
                  </p>
                  <div class="mt-6">
                    <router-link
                      to="/query"
                      class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                    >
                      Create New Query
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Element Details -->
          <ElementDetails 
            v-if="selectedElement"
            :element="selectedElement"
            @close="clearSelection"
            @highlight-neighbors="highlightNeighbors"
            @center-element="centerOnElement"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watchEffect } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import cytoscape from 'cytoscape'
import fcose from 'cytoscape-fcose'
import { 
  ExclamationCircleIcon,
  NoSymbolIcon 
} from '@heroicons/vue/24/outline'
import { 
  NetworkStats,
  NetworkFilters,
  NetworkToolbar,
  ElementDetails 
} from '@/components/visualization'
import { NetworkLayout } from '@/components/visualization/NetworkLayout'
import { NetworkAnalysis } from '@/components/visualization/NetworkAnalysis'
import { 
  nodeColors,
  edgeColors,
  generateNetworkStyle,
  visualizationDefaults 
} from '@/components/visualization/styles'

// Register cytoscape layouts
cytoscape.use(fcose)

// State
const router = useRouter()
const loading = ref(true)
const error = ref<string | null>(null)
const networkContainer = ref<HTMLElement | null>(null)
const cyInstance = ref<cytoscape.Core | null>(null)
const selectedElement = ref<any>(null)
const networkLayout = ref<NetworkLayout | null>(null)
const networkAnalysis = ref<NetworkAnalysis | null>(null)
const networkStats = ref({
  nodes: 0,
  edges: 0,
  density: 0,
  avgDegree: 0,
  clusters: 0
})

// Settings and Data
const dataSources = ['DisGeNET', 'STRING', 'KEGG']
const nodeTypes = ['Gene', 'Disease', 'Protein', 'Pathway']

// Computed
const hasData = computed(() => {
  return cyInstance.value?.elements().length > 0
})

// Network Initialization
onMounted(async () => {
  await initializeNetwork()
})

async function initializeNetwork() {
  try {
    loading.value = true
    error.value = null

    const identifierSetId = localStorage.getItem('currentIdentifierSetId')
    if (!identifierSetId) {
      loading.value = false
      return
    }

    // Load network data
    const response = await axios.get(`/api/identifiers/${identifierSetId}`)
    const networkData = response.data.combined_data

    // Initialize cytoscape
    if (networkContainer.value) {
      cyInstance.value = cytoscape({
        container: networkContainer.value,
        elements: transformDataToElements(networkData),
        style: generateNetworkStyle(),
        wheelSensitivity: visualizationDefaults.wheelSensitivity,
        minZoom: visualizationDefaults.minZoom,
        maxZoom: visualizationDefaults.maxZoom
      })

      // Initialize helpers
      networkLayout.value = new NetworkLayout(cyInstance.value)
      networkAnalysis.value = new NetworkAnalysis(cyInstance.value)

      // Set up event handlers
      setupEventHandlers()
      
      // Initial layout
      networkLayout.value.run('force')
      
      // Update stats
      updateNetworkStats()
    }
  } catch (err) {
    console.error('Error initializing network:', err)
    error.value = 'Failed to load network data'
  } finally {
    loading.value = false
  }
}

// Event Handlers
function setupEventHandlers() {
  if (!cyInstance.value) return

  cyInstance.value.on('tap', 'node, edge', (evt) => {
    selectedElement.value = {
      type: evt.target.isNode() ? 'node' : 'edge',
      data: evt.target.data()
    }
  })

  cyInstance.value.on('tap', (evt) => {
    if (evt.target === cyInstance.value) {
      selectedElement.value = null
    }
  })
}

// Network Actions
function handleLayoutChange(layout: string) {
  networkLayout.value?.run(layout)
}

function handleFilterUpdate(filters: any) {
  if (!networkLayout.value) return

  networkLayout.value.filterByType(
    Object.entries(filters.nodeTypes)
      .filter(([_, enabled]) => enabled)
      .map(([type]) => type)
  )
  networkLayout.value.filterEdgesByWeight(filters.edgeWeight)
  updateNetworkStats()
}

function handleZoom(action: string) {
  if (!cyInstance.value) return

  switch (action) {
    case 'Zoom In':
      cyInstance.value.zoom({
        level: cyInstance.value.zoom() * 1.2,
        renderedPosition: { x: cyInstance.value.width() / 2, y: cyInstance.value.height() / 2 }
      })
      break
    case 'Zoom Out':
      cyInstance.value.zoom({
        level: cyInstance.value.zoom() * 0.8,
        renderedPosition: { x: cyInstance.value.width() / 2, y: cyInstance.value.height() / 2 }
      })
      break
    case 'Fit':
      cyInstance.value.fit(undefined, 50)
      break
  }
}

async function handleExport(format: 'png' | 'json') {
  if (!cyInstance.value) return

  if (format === 'png') {
    const png = cyInstance.value.png({
      output: 'blob',
      bg: 'white',
      full: true,
      scale: 2
    })
    const url = URL.createObjectURL(png)
    const a = document.createElement('a')
    a.href = url
    a.download = 'network.png'
    a.click()
    URL.revokeObjectURL(url)
  } else {
    const json = cyInstance.value.json()
    const blob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'network.json'
    a.click()
    URL.revokeObjectURL(url)
  }
}

// Element Actions
function clearSelection() {
  selectedElement.value = null
  networkLayout.value?.clearHighlights()
}

function highlightNeighbors() {
  if (!selectedElement.value || !cyInstance.value) return
  const node = cyInstance.value.$id(selectedElement.value.data.id)
  networkLayout.value?.highlightNeighborhood(node)
}

function centerOnElement() {
  if (!selectedElement.value || !cyInstance.value) return
  const element = cyInstance.value.$id(selectedElement.value.data.id)
  networkLayout.value?.focusOnElement(element)
}

// Utilities
function transformDataToElements(data: any[]) {
  const nodes = new Map()
  const edges = []

  data.forEach(item => {
    switch (item.source) {
      case 'DisGeNET':
        addDisGeNETElements(item, nodes, edges)
        break
      case 'STRING':
        addSTRINGElements(item, nodes, edges)
        break
      case 'KEGG':
        addKEGGElements(item, nodes, edges)
        break
    }
  })

  return [...nodes.values(), ...edges]
}

function updateNetworkStats() {
  if (!networkAnalysis.value) return
  networkStats.value = networkAnalysis.value.getStatistics()
}

function retryLoading() {
  initializeNetwork()
}

// Cleanup
onBeforeUnmount(() => {
  networkLayout.value?.destroy()
  cyInstance.value?.destroy()
})
</script>

<style>
#cy {
  width: 100%;
  height: 100%;
}
</style>