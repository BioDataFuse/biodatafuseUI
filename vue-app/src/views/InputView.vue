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
          <h2 class="text-xl font-semibold text-white">Step 1: Import Your Identifiers</h2>
          <p class="mt-1 text-indigo-200">Provide your input and identifier type</p>
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
                      placeholder="e.g.&#10;DMD&#10;BRCA1&#10;TP53&#10;EGFR"
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
                  <label
                    class="flex flex-col w-full h-64 border-2 border-dashed border-indigo-300 rounded-lg hover:bg-gray-50 hover:border-indigo-400 transition-all cursor-pointer"
                    @dragover.prevent
                    @drop.prevent="handleDrop"
                  >
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
                      accept=".txt,.csv,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    />
                  </label>
                </div>
                <!-- Optional: User-defined Column Name -->
                <div class="flex justify-center items-center w-full">
                  <label class="flex flex-col w-full h-30 border-2 border-dashed border-indigo-300 rounded-lg hover:bg-gray-50 hover:border-indigo-400 transition-all">
                    <div class="flex flex-col items-center justify-center px-4 pt-7 text-center">
                      <label for="column-name" class="block text-sm font-medium text-gray-700">
                        Column name in file if not <code class="bg-gray-200 text-gray-800 px-1 rounded">identifier</code>
                      </label>
                      <input
                        id="column-name"
                        v-model="formData.columnName"
                        type="text"
                        placeholder="e.g., Gene or ID"
                        class="mt-4 block w-full max-w-sm rounded-md border border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      />
                      <p class="mt-2 text-xs text-gray-500">
                        If blank, defaults to <code class="bg-gray-100 px-1 rounded">identifier</code>
                      </p>
                    </div>
                  </label>
                </div>
              </div>
            </div>

            <!-- Settings Panel -->
            <div class="lg:col-span-2">
              <div class="bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden">
                <!-- Panel Header -->
                <div class="bg-gradient-to-r from-indigo-500/5 via-indigo-500/10 to-transparent px-6 py-5 border-b border-gray-100">
                  <div class="flex items-center space-x-3">
                    <div class="p-2 bg-white rounded-lg shadow-sm border border-indigo-100">
                      <BeakerIcon class="h-5 w-5 text-indigo-600" />
                    </div>
                    <div>
                      <h3 class="text-lg font-semibold text-gray-900">Input Settings</h3>
                      <p class="text-sm text-gray-500 mt-0.5">Configure your input parameters</p>
                    </div>
                  </div>
                </div>

                <div class="p-6">
                  <!-- Identifier Type Section -->
                  <div class="space-y-3">
                    <div class="flex items-center justify-between">
                      <div>
                        <label for="identifier-type" class="block text-sm font-medium text-gray-900">
                          Identifier Type
                        </label>
                        <p class="text-xs text-gray-500 mt-0.5">Select the format of your identifiers</p>
                      </div>
                      <div v-if="formData.identifierType" 
                          class="flex items-center space-x-1 text-indigo-600 bg-indigo-50 px-2 py-1 rounded">
                        <CheckCircleIcon class="h-4 w-4" />
                        <span class="text-xs font-medium">Selected</span>
                      </div>
                    </div>

                    <!-- Enhanced Select -->
                    <div class="relative mt-1 group">
                      <select
                        id="identifier-type"
                        v-model="formData.identifierType"
                        class="block w-full pl-4 pr-10 py-3 text-base border-2 border-gray-200 
                               rounded-lg bg-white shadow-sm appearance-none
                               focus:border-indigo-500 focus:ring focus:ring-indigo-200 
                               group-hover:border-gray-300
                               transition-all duration-200"
                      >
                        <option value="" disabled class="text-gray-500">Select type...</option>
                        <optgroup label="Gene Identifiers" class="font-semibold">
                          <option value="Ensembl" class="py-1.5">Ensembl Gene ID (e.g., ENSG00000012048)</option>
                          <option value="HGNC" class="py-1.5">HGNC Symbol (e.g., TP53)</option>
                          <option value="HGNC Accession Number" class="py-1.5">HGNC Accession (e.g., HGNC:11998)</option>
                          <option value="RefSeq" class="py-1.5">RefSeq ID (e.g., NM_001301717)</option>
                          <option value="NCBI Gene" class="py-1.5">NCBI Gene ID (e.g., 7157)</option>
                        </optgroup>
                        <optgroup label="Protein Identifiers" class="font-semibold">
                          <option value="Uniprot-TrEMBL" class="py-1.5">UniProtKB ID (e.g., P11532)</option>
                        </optgroup>
                        <optgroup label="Compound Identifiers" class="font-semibold">
                          <option value="HMDB" class="py-1.5">HMDB ID (e.g., HMDB0000001)</option>
                          <option value="ChEBI" class="py-1.5">ChEBI ID (e.g., CHEBI:15377)</option>
                          <option value="KEGG Compound" class="py-1.5">KEGG Compound (e.g., C00002)</option>
                          <option value="PubChem Compound" class="py-1.5">PubChem Compound (e.g., 100208)</option>
                        </optgroup>
                      </select>
                      <ChevronDownIcon class="absolute right-3 top-3.5 h-5 w-5 text-gray-400 
                                       group-hover:text-indigo-500 pointer-events-none transition-colors duration-200" />
                    </div>

                    <!-- Type Description -->
                    <div v-if="formData.identifierType" 
                         class="mt-3 bg-gray-50 rounded-lg px-4 py-3 border border-gray-200">
                      <div class="flex items-start space-x-3">
                        <InformationCircleIcon class="h-5 w-5 text-gray-400 mt-0.5 flex-shrink-0" />
                        <div>
                          <p class="text-sm text-gray-700">
                            {{ getIdentifierTypeDescription(formData.identifierType) }}
                          </p>
                        </div>
                      </div>
                    </div>

                    <!-- Validation Summary -->
                    <div v-if="!isFormValid" 
                         class="mt-4 bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                      <div class="flex">
                        <div class="flex-shrink-0">
                          <ExclamationTriangleIcon class="h-5 w-5 text-yellow-400" />
                        </div>
                        <div class="ml-3">
                          <h3 class="text-sm font-medium text-yellow-800">Required Fields</h3>
                          <ul class="mt-2 text-sm text-yellow-700 space-y-1">
                            <li v-if="!hasInput" class="flex items-center">
                              <MinusIcon class="h-4 w-4 text-yellow-400 mr-2" />
                              <span>Enter identifiers or upload a file</span>
                            </li>
                            <li v-if="!formData.identifierType" class="flex items-center">
                              <MinusIcon class="h-4 w-4 text-yellow-400 mr-2" />
                              <span>Select identifier type</span>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </div>

                    <!-- Submit Button -->
                    <button
                      type="button"
                      @click="submitForm"
                      :disabled="loading || !isFormValid"
                      class="relative w-full flex justify-center items-center px-4 py-3 mt-6
                             border border-transparent text-sm font-semibold rounded-lg shadow-sm 
                             text-white bg-indigo-600 hover:bg-indigo-700 
                             focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 
                             disabled:opacity-50 disabled:cursor-not-allowed 
                             transition-colors duration-200"
                    >
                      <span v-if="loading" class="flex items-center">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                        </svg>
                        Processing...
                      </span>
                      <span v-else class="flex items-center">
                        Continue to Mapping
                        <ArrowRightIcon class="ml-2 -mr-1 h-5 w-5" />
                      </span>
                    </button>
                  </div>
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
  BeakerIcon,
  ChevronDownIcon,
  ArrowRightIcon,
  CheckCircleIcon,
  InformationCircleIcon,
  MinusIcon,
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
  { name: 'Identifier Mapping', status: 'upcoming' },
  { name: 'Select Data Sources', status: 'upcoming' },
  { name: 'Annotations', status: 'upcoming' },
  // { name: 'Visualize', status: 'upcoming' }
]

const currentStep = ref(0)

const formData = ref({
  textInput: '',
  identifierType: '',
  file: null,
  columnName: ''
})

const hasInput = computed(() => {
  return formData.value.textInput.trim() || selectedFile.value
})

const isFormValid = computed(() => {
  return hasInput.value && formData.value.identifierType
})

const getInputSummary = computed(() => {
  const input = formData.value.textInput.trim()
  if (!input) return 'No text input'
  
  const lines = input.split('\n').filter(line => line.trim())
  const count = lines.length
  
  if (count === 0) return 'No identifiers entered'
  if (count === 1) return '1 identifier entered'
  return `${count} identifiers entered`
})

function getIdentifierTypeDescription(type) {
  const descriptions = {
    'Ensembl': 'Standard stable identifier format for genes, transcripts, and proteins from the Ensembl database.',
    'HGNC': 'Human Gene Nomenclature Committee approved gene symbols and names.',
    'HGNC Accession Number': 'Unique identifiers assigned by Human Gene Nomenclature Committee to human genes.',
    'NCBI Gene': 'Unique identifiers from the NCBI Gene Database.',
    'RefSeq': 'Reference sequence standards from NCBI Reference Sequence Database.',
    'HMDB': 'Human Metabolome Database compound identifiers.',
    'ChEBI': 'Chemical Entities of Biological Interest standardized identifiers.',
    'SMILES': 'Simplified Molecular Input Line Entry System notation.'
  }
  return descriptions[type] || 'Standard identifier format'
}

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    // Validate file type
    const validTypes = [
      'text/plain',
      'text/csv',
      'application/vnd.ms-excel',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    ]
    if (!validTypes.includes(file.type)) {
      error.value = 'Please upload a TXT, CSV or Excel file'
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
    error.value = null
  }
}

function handleDrop(event) {
  const file = event.dataTransfer.files[0]
  if (file) {
    const fakeEvent = { target: { files: [file] } }
    handleFileUpload(fakeEvent)
  }
}

// Submit form
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

    if (formData.value.columnName.trim()) {
      form.append('column_name', formData.value.columnName.trim())
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