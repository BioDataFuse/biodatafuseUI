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
          <h2 class="text-xl font-semibold text-white">Step 3: Annotation Results</h2>
          <p class="mt-1 text-indigo-200">Review the annotation results before continueing to visualization.</p>
          <p class="mt-1 text-indigo-200">
            <strong>Note: </strong> You can go back to the previous step to modify your query.
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="mt-8 text-center">
          <div class="inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md text-white bg-indigo-500">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
            Processing visualization...
          </div>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="mt-8 rounded-md bg-red-50 p-4">
          <div class="flex">
            <ExclamationCircleIcon class="h-5 w-5 text-red-400" aria-hidden="true" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-red-800">{{ error }}</h3>
            </div>
          </div>
        </div>

        <!-- Results Table -->
        <div v-else-if="annotationResults" class="mt-8">
          <div class="bg-white shadow sm:rounded-lg">
            <div class="px-4 py-5 sm:p-6">

              <!-- Annotation Results Table -->
              <!-- Filter Controls -->
              <div class="mt-1 space-y-4">
                <div class="flex flex-col sm:flex-row sm:space-x-6 sm:items-end">
                  <!-- Select Input ID -->
                  <div class="w-full sm:w-1/2">
                    <label class="block text-xl font-medium text-gray-700">Select Input</label>
                    <select v-model="selectedInputId" class="block w-full rounded-md border-gray-300 shadow-sm sm:text-sm">
                      <option disabled value="">-- Choose Input ID --</option>
                      <option v-for="id in availableInputIds" :key="id" :value="id">{{ id }}</option>
                    </select>
                  </div>

                  <!-- Select Data Source -->
                  <div class="w-full sm:w-1/2" v-if="selectedInputId">
                    <label class="block text-xl font-medium text-gray-700">Select Data Source</label>
                    <select v-model="selectedDataSource" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm">
                      <option disabled value="">-- Choose Data Source --</option>
                      <option v-for="datasource in availableDataSources" :key="datasource" :value="datasource">{{ datasource }}</option>
                    </select>
                  </div>
                </div>
              </div>

              <!-- Focused Table Display -->
              <div v-if="selectedDataSourceData.length" class="mt-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-2 text-left">
                  Annotation results for 
                  <span class="underline font-bold">{{ selectedInputId }}</span> 
                  : {{ selectedDataSource }}
                </h3>
                <table class="min-w-full divide-y divide-gray-200 text-sm text-gray-700 border rounded">
                  <thead>
                    <tr>
                      <th
                        v-for="(v, key, i) in selectedDataSourceData[0]"
                        :key="`header-${key}-${i}`"
                        class="px-2 py-1 font-semibold border-b text-left !text-left"
                      >
                        {{ key }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(entry, idx) in selectedDataSourceData" :key="idx" class="border-t">
                      <td
                        v-for="(val, k) in entry"
                        :key="`cell-${idx}-${k}`"
                        class="px-2 py-1 border-b text-left !text-left"
                      >
                        {{ val }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <!-- Navigation Buttons -->
              <div class="mt-8 flex justify-between">
                <button
                  type="button"
                  @click="goBack"
                  class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                >
                  Back to data source selection 
                </button>
                <button
                  type="button"
                  @click="continueToVisualize"
                  class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
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
import { useRouter } from 'vue-router'
import { ExclamationCircleIcon, ArrowRightIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const loading = ref(true)
const error = ref(null)
const annotationResults = ref(null)

const steps = [
  { name: 'Input Identifiers', status: 'complete' },
  { name: 'Identifier Mapping', status: 'complete' },
  { name: 'Select Data Sources', status: 'complete' },
  { name: 'Annotations', status: 'current' },
  { name: 'Visualize', status: 'upcoming' }
]

const currentStep = ref(3)
const fixedFields = ["identifier", "identifier.source", "target", "target.source"]

const selectedInputId = ref('')
const selectedDataSource = ref('')

const availableInputIds = computed(() => {
  return Object.values(annotationResults.value?.combined_df || {}).map(item => item.identifier)
})


const availableDataSources = computed(() => {
  const inputId = selectedInputId.value
  if (!inputId) return []

  const row = Object.values(annotationResults.value?.combined_df || {}).find(item => item.identifier === inputId)
  return Object.keys(row).filter(k => !fixedFields.includes(k) && Array.isArray(row[k]))
})

const selectedDataSourceData = computed(() => {
  if (!selectedInputId.value || !selectedDataSource.value) return []
  const selectedRow = Object.values(annotationResults.value?.combined_df || {}).find(item => item.identifier === selectedInputId.value)
  return selectedRow ? selectedRow[selectedDataSource.value] : []
})


onMounted(() => {
  const stored = localStorage.getItem('annotationResults')
  if (stored) {
    try {
      annotationResults.value = JSON.parse(stored)
    } catch (e) {
      error.value = 'Failed to parse annotation results.'
      console.error("JSON parse error:", e)
    }
  } else {
    router.push('/query/datasources')
  }
  loading.value = false
})

function goBack() {
  router.push('/query/datasources')
}

function continueToVisualize() {
  router.push('/query/visualize')
}
</script>
