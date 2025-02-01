<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="px-4 sm:px-0">
        <h2 class="text-2xl font-bold leading-7 text-gray-900 sm:truncate sm:text-3xl sm:tracking-tight">
          Identifier Mapping Results
        </h2>
        <p class="mt-1 max-w-2xl text-sm leading-6 text-gray-500">
          Review the mapped identifiers before proceeding to database selection.
        </p>
      </div>

      <!-- Progress Steps -->
      <div class="mt-8">
        <nav aria-label="Progress">
          <ol role="list" class="space-y-4 md:flex md:space-y-0 md:space-x-8">
            <li v-for="(step, index) in steps" :key="step.name" class="md:flex-1">
              <div class="flex flex-col border-l-4 border-indigo-600 py-2 pl-4 md:border-l-0 md:border-t-4 md:pb-0 md:pl-0 md:pt-4">
                <span :class="[
                  index <= currentStep ? 'text-indigo-600' : 'text-gray-500',
                  'text-sm font-medium'
                ]">Step {{ index + 1 }}</span>
                <span class="text-sm font-medium">{{ step.name }}</span>
              </div>
            </li>
          </ol>
        </nav>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="mt-8 text-center">
        <div class="inline-flex items-center px-4 py-2 font-semibold leading-6 text-sm shadow rounded-md text-white bg-indigo-500">
          <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          Processing mappings...
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
      <div v-else-if="mappingResults" class="mt-8">
        <div class="bg-white shadow sm:rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <!-- Summary Stats -->
            <dl class="grid grid-cols-1 gap-5 sm:grid-cols-3">
              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <dt class="text-sm font-medium text-gray-500">Total Identifiers</dt>
                  <dd class="mt-1 text-3xl font-semibold text-gray-900">
                    {{ mappingResults.input_identifiers?.length || 0 }}
                  </dd>
                </div>
              </div>
              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <dt class="text-sm font-medium text-gray-500">Mapped Successfully</dt>
                  <dd class="mt-1 text-3xl font-semibold text-green-600">
                    {{ Object.keys(mappingResults.mapped_identifiers || {}).length }}
                  </dd>
                </div>
              </div>
              <div class="bg-white overflow-hidden shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                  <dt class="text-sm font-medium text-gray-500">Mapping Type</dt>
                  <dd class="mt-1 text-3xl font-semibold text-gray-900">
                    {{ mappingResults.identifier_type }}
                  </dd>
                </div>
              </div>
            </dl>

            <!-- Mapping Results Table -->
            <div class="mt-8 flow-root">
              <div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
                <div class="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
                  <table class="min-w-full divide-y divide-gray-300">
                    <thead>
                      <tr>
                        <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">Input ID</th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Ensembl</th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">HGNC</th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">NCBI</th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">UniProt</th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                      <tr v-for="(mappings, inputId) in mappingResults.mapped_identifiers" :key="inputId">
                        <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900">{{ inputId }}</td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ mappings.ensembl || '-' }}</td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ mappings.hgnc || '-' }}</td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ mappings.ncbi || '-' }}</td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{{ mappings.uniprot || '-' }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            <!-- Navigation Buttons -->
            <div class="mt-8 flex justify-between">
              <button
                type="button"
                @click="goBack"
                class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
              >
                Back to Input
              </button>
              <button
                type="button"
                @click="continueToDataSources"
                class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              >
                Continue to Data Sources
                <ArrowRightIcon class="ml-2 -mr-0.5 h-4 w-4" aria-hidden="true" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ExclamationCircleIcon, ArrowRightIcon } from '@heroicons/vue/24/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(true)
const error = ref(null)
const mappingResults = ref(null)

const steps = [
  { name: 'Input Identifiers', status: 'complete' },
  { name: 'Map IDs', status: 'current' },
  { name: 'Select Sources', status: 'upcoming' },
  { name: 'Visualize', status: 'upcoming' }
]

const currentStep = ref(1) // We're on the second step

// Get identifier set ID from localStorage
const identifierSetId = localStorage.getItem('currentIdentifierSetId')

onMounted(async () => {
  if (!identifierSetId) {
    router.push('/query')
    return
  }

  try {
    const response = await axios.get(`/api/identifiers/${identifierSetId}`)
    mappingResults.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error loading mapping results'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
})

function goBack() {
  router.push('/query')
}

function continueToDataSources() {
  router.push('/query/datasources')
}
</script>