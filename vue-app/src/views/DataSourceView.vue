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
            Build your biological query and visualize the output in four simple steps
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
          <p class="mt-1 text-indigo-200">Choose the biological databases to query for your analysis.</p>
        </div>

        <!-- Main Content -->
        <div class="mt-8 bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <form @submit.prevent="submitForm">
              <!-- Data Sources Selection -->
              <div class="space-y-4">
                <div v-for="source in availableSources" :key="source.id" class="flex items-start">
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
                    
                    <!-- API Key Input Field (shown if source requires API key and is selected) -->
                    <div v-if="source.requiresApiKey && selectedSources.includes(source.id)" class="mt-2">
                      <label :for="source.id + '-api-key'" class="block text-sm font-medium text-gray-700">
                        {{ source.name }} API Key
                      </label>
                      <input
                        :id="source.id + '-api-key'"
                        type="password"
                        v-model="sourceApiKeys[source.id]"
                        class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                        :placeholder="'Enter your ' + source.name + ' API key'"
                      />
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
              <div class="mt-6 flex justify-between">
                <button
                  type="button"
                  class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                  @click="goBack"
                >
                  Back to Mapping
                </button>
                <button
                  type="submit"
                  :disabled="loading || !isFormValid"
                  class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50"
                >
                  <span v-if="loading">Processing...</span>
                  <span v-else>Continue to Analysis</span>
                  <ArrowRightIcon class="ml-2 -mr-0.5 h-4 w-4" aria-hidden="true" />
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Processing Results -->
        <div v-if="results" class="mt-8 bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg font-medium leading-6 text-gray-900">Processing Results</h3>
            <div class="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
              <!-- Summary Stats -->
              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <dt class="text-sm font-medium text-gray-500">Total Associations</dt>
                  <dd class="mt-1 text-3xl font-semibold text-gray-900">
                    {{ results.metadata.total_associations }}
                  </dd>
                </div>
              </div>

              <!-- Sources Processed -->
              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <dt class="text-sm font-medium text-gray-500">Sources Processed</dt>
                  <dd class="mt-1 text-sm text-gray-900">
                    <ul class="list-disc pl-5">
                      <li v-for="source in results.metadata.sources_processed" :key="source">
                        {{ source }}
                      </li>
                    </ul>
                  </dd>
                </div>
              </div>

              <!-- Continue Button -->
              <div class="col-span-full mt-4">
                <button
                  type="button"
                  @click="continueToVisualization"
                  class="inline-flex items-center rounded-md bg-indigo-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                  Continue to Visualization
                  <ArrowRightIcon class="ml-2 -mr-0.5 h-4 w-4" aria-hidden="true" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ExclamationCircleIcon, ArrowRightIcon } from '@heroicons/vue/24/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const availableSources = ref([])
const selectedSources = ref([])
const sourceApiKeys = ref({})
const loading = ref(false)
const error = ref(null)
const results = ref(null)

const steps = [
  { name: 'Input Identifiers', status: 'complete' },
  { name: 'Identifier Mapping', status: 'complete' },
  { name: 'Select Sources', status: 'current' },
  { name: 'Visualize', status: 'upcoming' }
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

// Load available data sources on mount
onMounted(async () => {
  if (!identifierSetId) {
    router.push('/query')
    return
  }

  try {
    const response = await axios.get('/api/datasources')
    availableSources.value = response.data.map(source => ({
      ...source,
      requiresApiKey: source.requires_key // Use the requires_key property from backend
    }))
  } catch (err) {
    error.value = 'Error loading data sources: ' + (err.response?.data?.detail || err.message)
    console.error('Error:', err)
  }
})

// Submit form
async function submitForm() {
  if (!isFormValid.value) return

  try {
    error.value = null
    loading.value = true

    // Create array of selected sources with their API keys
    const datasources = selectedSources.value.map(sourceId => {
      const apiKey = sourceApiKeys.value[sourceId]
      return {
        source: sourceId,
        ...(apiKey ? { api_key: apiKey } : {}) // Only include api_key if it exists
      }
    })

    // Send array directly as expected by the API
    const response = await axios.post(`/api/datasources/${identifierSetId}/process`, datasources)

    if (response.data.status === 'success') {
      results.value = response.data
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

// Navigation functions
function goBack() {
  router.push('/query/mapping')
}

function continueToVisualization() {
  router.push('/visualization')
}
</script>