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
            Build your biological query in three simple steps
          </p>
        </div>

        <!-- Steps Progress -->
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
          <h2 class="text-xl font-semibold text-white">Step 1: Import Your Identifiers</h2>
          <p class="mt-1 text-indigo-200">Choose your input method and identifier type</p>
        </div>

        <div class="p-6">
          <!-- Input Method Tabs -->
          <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-8" aria-label="Tabs">
              <button
                v-for="tab in tabs"
                :key="tab.name"
                @click="activeTab = tab.id"
                :class="[
                  activeTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                  'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center'
                ]"
              >
                <component :is="tab.icon" class="h-5 w-5 mr-2" />
                {{ tab.name }}
              </button>
            </nav>
          </div>

          <div class="mt-6 grid grid-cols-1 lg:grid-cols-5 gap-8">
            <!-- Input Section -->
            <div class="lg:col-span-3">
              <!-- Text Input -->
              <div v-show="activeTab === 'text'" class="space-y-4">
                <div>
                  <label for="text-input" class="block text-sm font-medium text-gray-700">
                    Enter identifiers (one per line)
                  </label>
                  <div class="mt-1">
                    <textarea
                      id="text-input"
                      v-model="formData.textInput"
                      rows="10"
                      class="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border border-gray-300 rounded-lg"
                      placeholder="e.g.&#10;BRCA1&#10;TP53&#10;EGFR"
                    ></textarea>
                  </div>
                  <p class="mt-2 text-sm text-gray-500">
                    Enter each identifier on a new line
                  </p>
                </div>
              </div>

              <!-- File Upload -->
              <div v-show="activeTab === 'file'" class="space-y-4">
                <div class="flex justify-center items-center w-full">
                  <label class="flex flex-col w-full h-64 border-2 border-dashed border-indigo-300 rounded-lg hover:bg-gray-50 hover:border-indigo-400 transition-all cursor-pointer">
                    <div class="flex flex-col items-center justify-center pt-7">
                      <DocumentArrowUpIcon v-if="!selectedFile" class="w-12 h-12 text-indigo-400" />
                      <DocumentCheckIcon v-else class="w-12 h-12 text-green-500" />
                      <p class="pt-4 text-sm tracking-wider text-gray-600">
                        <span v-if="!selectedFile">
                          Drag and drop your file here or click to select
                        </span>
                        <span v-else class="text-green-600 font-medium">
                          {{ selectedFile.name }}
                        </span>
                      </p>
                      <p class="pt-2 text-xs text-gray-500">
                        Support for CSV or TXT files up to 10MB
                      </p>
                    </div>
                    <input
                      type="file"
                      class="hidden"
                      @change="handleFileUpload"
                      accept=".txt,.csv"
                    />
                  </label>
                </div>
              </div>
            </div>

            <!-- Settings Panel -->
            <div class="lg:col-span-2">
              <div class="bg-gray-50 rounded-lg p-6">
                <h3 class="text-lg font-medium text-gray-900 mb-4">Query Settings</h3>

                <!-- Identifier Type Selection -->
                <div class="space-y-4">
                  <div>
                    <label for="identifier-type" class="block text-sm font-medium text-gray-700">
                      Identifier Type
                    </label>
                    <select
                      id="identifier-type"
                      v-model="formData.identifierType"
                      class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md"
                    >
                      <option value="" disabled>Select type</option>
                      <optgroup label="Gene Identifiers">
                        <option value="Ensembl">Ensembl</option>
                        <option value="HGNC">HGNC Symbol</option>
                        <option value="HGNC Accession Number">HGNC Accession Number</option>
                        <option value="RefSeq">RefSeq</option>
                        <option value="NCBI Gene">NCBI Gene</option>
                      </optgroup>
                      <optgroup label="Compound Identifiers">
                        <option value="HMDB">HMDB</option>
                        <option value="ChEBI">ChEBI</option>
                        <option value="SMILES">SMILES</option>
                      </optgroup>
                    </select>
                  </div>

                  <!-- Validation Summary -->
                  <div class="rounded-md bg-yellow-50 p-4" v-if="!isFormValid">
                    <div class="flex">
                      <ExclamationTriangleIcon class="h-5 w-5 text-yellow-400" />
                      <div class="ml-3">
                        <h3 class="text-sm font-medium text-yellow-800">Required:</h3>
                        <ul class="mt-2 text-sm text-yellow-700 list-disc pl-5">
                          <li v-if="!hasInput">Enter identifiers or upload a file</li>
                          <li v-if="!formData.identifierType">Select identifier type</li>
                        </ul>
                      </div>
                    </div>
                  </div>

                  <!-- Submit Button -->
                  <button
                    type="button"
                    @click="submitForm"
                    :disabled="loading || !isFormValid"
                    class="w-full flex justify-center items-center px-4 py-3 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span v-if="loading" class="flex items-center">
                      <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                      </svg>
                      Processing...
                    </span>
                    <span v-else>Continue to Mapping</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="mt-6 rounded-md bg-red-50 p-4">
        <div class="flex">
          <XCircleIcon class="h-5 w-5 text-red-400" />
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">{{ error }}</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  DocumentArrowUpIcon,
  DocumentCheckIcon,
  DocumentTextIcon,
  ExclamationTriangleIcon,
  XCircleIcon,
  ArrowUpTrayIcon,
} from '@heroicons/vue/24/outline'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const error = ref(null)
const selectedFile = ref(null)
const activeTab = ref('text')

const tabs = [
  { id: 'text', name: 'Text Input', icon: DocumentTextIcon },
  { id: 'file', name: 'File Upload', icon: ArrowUpTrayIcon },
]

const steps = [
  { name: 'Input Identifiers', status: 'current' },
  { name: 'Map IDs', status: 'upcoming' },
  { name: 'Select Sources', status: 'upcoming' }
]

const currentStep = ref(0)

const formData = ref({
  textInput: '',
  identifierType: '',
  file: null
})

const hasInput = computed(() => {
  return formData.value.textInput.trim() || selectedFile.value
})

const isFormValid = computed(() => {
  return hasInput.value && formData.value.identifierType
})

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    // Validate file type
    const validTypes = ['text/plain', 'text/csv']
    if (!validTypes.includes(file.type)) {
      error.value = 'Please upload a TXT or CSV file'
      event.target.value = ''
      selectedFile.value = null
      return
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      error.value = 'File size must be less than 10MB'
      event.target.value = ''
      selectedFile.value = null
      return
    }

    selectedFile.value = file
    formData.value.file = file
  }
}

async function submitForm() {
  if (!isFormValid.value) return

  error.value = null
  loading.value = true

  try {
    const form = new FormData()
    form.append('identifier_type', formData.value.identifierType)
    
    if (formData.value.textInput.trim()) {
      form.append('text_input', formData.value.textInput)
    }
    
    if (formData.value.file) {
      form.append('file', formData.value.file)
    }

    const response = await axios.post('/api/identifiers', form, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    // Store the identifier set ID for the next step
    localStorage.setItem('currentIdentifierSetId', response.data.set_id)
    
    // Navigate to mapping results
    router.push('/query/mapping')

  } catch (err) {
    error.value = err.response?.data?.detail || 'Error processing identifiers'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}
</script>