<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Header Section with Steps -->
      <div class="mb-10">
        <div class="text-center">
          <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
            Query Builder
          </h1>
          <p class="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
            Build your biological query and explore the output in four simple steps
          </p>
        </div>

        <!-- Progress Steps -->
        <div class="mt-8">
          <div class="relative">
            <div class="absolute inset-0 flex items-center" aria-hidden="true">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-between">
              <div v-for="(step, index) in steps" :key="step.name"
                   :class="[
                     index <= currentStep ? 'text-indigo-600' : 'text-gray-500',
                     'bg-white px-4 py-2 rounded-full shadow-sm border border-gray-200'
                   ]">
                <span class="font-medium">{{ step.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Area -->
      <div class="mt-12 bg-white rounded-2xl shadow-xl overflow-hidden">
        <!-- Top Bar -->
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-800 px-6 py-4">
          <h2 class="text-xl font-semibold text-white">Step 3: Select Data Sources</h2>
          <p class="mt-1 text-indigo-200">Choose the biological data sources to query for your analysis.</p>
          <p class="mt-1 text-indigo-200"> <strong>Note: </strong>Some sources may require an API key for access. </p>
          <!-- Missing Database Note -->
          <div class="mt-4 p-4 bg-gray-100 rounded-lg border border-gray-300">
            <p class="text-sm text-gray-700">
              <strong>Missing a data source?</strong> If there's a biological data source you'd like us to support, please
              <a
                href="https://github.com/BioDataFuse/pyBiodatafuse/issues/new?labels=enhancement&template=new_datasource_request.yaml"
                target="_blank"
                rel="noopener noreferrer"
                class="text-indigo-600 underline hover:text-indigo-800"
              >
                create a feature request on GitHub
              </a>.
            </p>
          </div>

        </div>

        <!-- Main Content -->
        <div class="mt-8 bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <form @submit.prevent="submitForm">
              <!-- Data Sources Selection -->
              <div class="space-y-4">
                <div v-for="(group, category) in groupedSources" :key="category" class="mb-8">
                  <h3 class="text-lg font-semibold text-indigo-700 mb-2">
                    Data Sources for annotating {{ category }} input
                  </h3>

                  <div v-for="source in group" :key="source.id" class="flex items-start border-b border-gray-200 pb-4 mb-4">
                    <div class="flex h-6 items-center">
                      <input
                        :id="source.id"
                        type="checkbox"
                        v-model="selectedSources"
                        :value="source.id"
                        class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-600"
                      />
                    </div>
                    <div class="ml-3 flex-grow">
                      <label :for="source.id" class="font-medium text-gray-700">{{ source.name }}</label>
                      <p class="text-sm text-gray-500">{{ source.description }}</p>
                      
                      <!-- Source metadata (version & endpoint) -->
                      <p v-if="getSourceMetadata(source.id) && (getSourceMetadata(source.id).version || getSourceMetadata(source.id).endpoint)" class="text-xs text-gray-400 mt-1">
                        <span v-if="getSourceMetadata(source.id).version && getSourceMetadata(source.id).version !== 'unknown'">
                          Version: {{ getSourceMetadata(source.id).version }}
                        </span>
                        <span v-if="getSourceMetadata(source.id).version && getSourceMetadata(source.id).version !== 'unknown' && getSourceMetadata(source.id).endpoint"> · </span>
                        <span v-if="getSourceMetadata(source.id).endpoint">
                          Endpoint: <a :href="getSourceMetadata(source.id).endpoint" target="_blank" rel="noopener noreferrer" class="hover:text-indigo-500">{{ getSourceMetadata(source.id).endpoint }}</a>
                        </span>
                      </p>

                      <!-- API key input with optional link -->
                      <div v-if="source.requiresApiKey && selectedSources.includes(source.id)" class="mt-2">
                        <label :for="source.id + '-api-key'" class="block text-sm font-medium text-gray-700">
                          {{ source.name }} API key
                          <a
                            v-if="source.id === 'disgenet'"
                            href="https://disgenet.com/plans"
                            target="_blank"
                            rel="noopener noreferrer"
                            class="ml-2 text-indigo-600 hover:underline text-xs"
                          >
                            (see plans)
                          </a>
                        </label>
                        <input
                          :id="source.id + '-api-key'"
                          type="password"
                          v-model="sourceApiKeys[source.id]"
                          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                          :placeholder="'Enter your ' + source.name + ' API key'"
                        />
                      </div>

                      <!-- Map name input with optional link -->
                      <div v-if="source.requiresMapName && selectedSources.includes(source.id)" class="mt-2">
                        <label :for="source.id + '-map-name'" class="block text-sm font-medium text-gray-700">
                          {{ source.name }} map name
                          <a
                            v-if="source.id === 'minerva'"
                            href="https://minerva-net.lcsb.uni.lu/table.html"
                            target="_blank"
                            rel="noopener noreferrer"
                            class="ml-2 text-indigo-600 hover:underline text-xs"
                          >
                            (see the "map name" column in the extensive list)
                          </a>
                        </label>
                        <input
                          :id="source.id + '-map-name'"
                          type="text"
                          v-model="sourceMapName[source.id]"
                          class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                          :placeholder="'Enter ' + source.name + ' map name, e.g. COVID19 Disease Map'"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Error Display -->
              <div v-if="error" class="mt-4 rounded-md bg-red-50 p-4">
                <div class="flex">
                  <ExclamationCircleIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
                  <div class="ml-3">
                    <h3 class="text-sm font-medium text-red-800">{{ error }}</h3>
                  </div>
                </div>
              </div>

              <!-- Navigation Buttons -->
              <div class="mt-8 flex justify-between">
                <button
                  type="button"
                  class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  @click="goBack"
                >
                  Back to Input
                </button>
                <button
                  type="button"
                  @click="continueToAnnotations"
                  :disabled="loading || !isFormValid"
                  class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50"
                >
                  <span v-if="loading">Processing...</span>
                  <span v-else>Continue to Annotation</span>
                  <ArrowRightIcon class="ml-2 -mr-0.5 h-4 w-4" aria-hidden="true" />
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ExclamationCircleIcon, ArrowRightIcon } from '@heroicons/vue/24/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const availableSources = ref([])
const selectedSources = ref([])
const sourceApiKeys = ref({})
const sourceMapName = ref({})
const loading = ref(false)
const error = ref(null)
const results = ref(null)
const sourceMetadata = ref({}) // Map of source id to metadata (version, endpoint)

const steps = [
  { name: 'Input Identifiers', status: 'complete' },
  { name: 'Identifier Mapping', status: 'complete' },
  { name: 'Select Data Sources', status: 'current' },
  { name: 'Annotations', status: 'upcoming' },
  // { name: 'Visualize', status: 'upcoming' }
]

const currentStep = ref(2)

// Get identifier set ID from localStorage
const identifierSetId = localStorage.getItem('currentIdentifierSetId')

// Form validation
const isFormValid = computed(() => {
  if (selectedSources.value.length === 0) return false
  
  // Check if all selected sources that require API keys have them
  const hasAllRequiredKeys = selectedSources.value.every(sourceId => {
    const source = availableSources.value.find(s => s.id === sourceId)
    if (!source) return false
    return !source.requiresApiKey || (source.requiresApiKey && sourceApiKeys.value[sourceId])
  })

  
  return hasAllRequiredKeys
})

// Helper function to get metadata for a source
const getSourceMetadata = (sourceId) => {
  // Map UI source IDs to metadata source IDs
  const idMap = {
    'wikipathways_pathways': 'wikipathways',
    'wikipathways_interactions': 'wikipathways',
    'opentargets_disease_compound': 'opentargets',
    'opentargets_go': 'opentargets',
    'opentargets_reactome': 'opentargets',
    'opentargets_gene_compound': 'opentargets',
    'intact_gene_interactions': 'intact',
    'intact_compound_interactions': 'intact',
    'molmedb_compounds': 'molmedb',
    'molmedb_gene': 'molmedb',
    'pubchem_assays': 'pubchem',
    'aop_wiki_rdf': 'aopwiki',
  }
  const metaId = idMap[sourceId] || sourceId
  return sourceMetadata.value[metaId] || null
}

// Load available data sources on mount
onMounted(async () => {
  if (!identifierSetId) {
    router.push('/query')
    return
  }

  try {
    // Fetch both datasources and metadata in parallel
    const [sourcesResponse, metadataResponse] = await Promise.all([
      axios.get('/api/datasources'),
      axios.get('/api/datasources/metadata').catch(() => ({ data: [] }))
    ])
    
    availableSources.value = sourcesResponse.data.map(source => ({
      ...source,
      requiresApiKey: source.requires_key,
      requiresMapName: source.requires_map_name
    }))
    
    // Build metadata map
    metadataResponse.data.forEach(meta => {
      sourceMetadata.value[meta.id] = meta
    })
  } catch (err) {
    error.value = 'Error loading data sources: ' + (err.response?.data?.detail || err.message)
    console.error('Error:', err)
  }
})

const groupedSources = computed(() => {
  const groups = {
    gene: [],
    compound: [],
    'both gene and compound': []
  }

  availableSources.value.forEach(source => {
    // Hide opentargets_disease_compound if disgenet is not selected
    if (
      source.id === 'opentargets_disease_compound' &&
      !selectedSources.value.includes('disgenet')
    ) {
      return // skip rendering this source
    }

    const category = source.category
    if (!groups[category]) groups[category] = []
    groups[category].push(source)
  })

  return groups
})

watch(selectedSources, (newSelection) => {
  const hasDisgenet = newSelection.includes('disgenet')
  const hasOTDC = newSelection.includes('opentargets_disease_compound')

  if (!hasDisgenet && hasOTDC) {
    // Remove opentargets_disease_compound if disgenet was unchecked
    const index = selectedSources.value.indexOf('opentargets_disease_compound')
    if (index !== -1) {
      selectedSources.value.splice(index, 1)
    }
  }
})


// Navigation functions
async function continueToAnnotations() {
  if (!isFormValid.value) return

  try {
    error.value = null
    loading.value = true

    // Create array of selected sources with their API keys
    const datasources = selectedSources.value.map(sourceId => {
      const apiKey = sourceApiKeys.value[sourceId]
      const mapName = sourceMapName.value[sourceId]
      return {
        source: sourceId,
        ...(apiKey ? { api_key: apiKey } : {}), // Only include api_key if it exists
        ...(mapName ? { map_name: mapName } : {}) // Only include map_name if it exists
      }
    })

    console.log(datasources); 

    // Send array directly as expected by the API

    const response = await axios.post(`/api/datasources/${identifierSetId}/process`, datasources)
    // throw new Error(response.data.status)

    if (response.data.status === 'completed') {
      results.value = response.data
      // Don't store full results in localStorage - they may exceed quota for large payloads
      // Results will be fetched from the API in AnnotationResultsView using the identifier set ID
      // which is already stored as 'currentIdentifierSetId'
      router.push('/query/annotations');
    } else {
      throw new Error(response.data.message || 'Processing failed')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || err.message || 'Error processing data sources'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}
function goBack() {
  router.push('/query')
}
</script>