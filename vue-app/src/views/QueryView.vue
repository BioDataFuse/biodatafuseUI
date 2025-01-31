<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 sm:px-0">
      <h2 class="text-2xl font-semibold text-gray-900">Query Biological Databases</h2>
      <p class="mt-1 text-sm text-gray-600">
        Search and integrate data from multiple biological databases.
      </p>
    </div>

    <div class="mt-6">
      <div class="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
        <div class="md:grid md:grid-cols-3 md:gap-6">
          <div class="md:col-span-1">
            <h3 class="text-lg font-medium leading-6 text-gray-900">Input Parameters</h3>
            <p class="mt-1 text-sm text-gray-500">
              Enter identifiers or upload a file to query the databases.
            </p>
          </div>
          
          <div class="mt-5 md:mt-0 md:col-span-2">
            <form @submit.prevent="submitQuery">
              <!-- Input Type Selection -->
              <div class="grid grid-cols-6 gap-6">
                <div class="col-span-6 sm:col-span-3">
                  <label for="input-type" class="block text-sm font-medium text-gray-700">Input Type</label>
                  <select
                    id="input-type"
                    v-model="inputType"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  >
                    <option value="text">Text Input</option>
                    <option value="file">File Upload</option>
                  </select>
                </div>

                <div class="col-span-6 sm:col-span-3">
                  <label for="identifier-type" class="block text-sm font-medium text-gray-700">Identifier Type</label>
                  <select
                    id="identifier-type"
                    v-model="identifierType"
                    class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  >
                    <option value="gene">Gene Symbol</option>
                    <option value="protein">Protein ID</option>
                    <option value="disease">Disease ID</option>
                  </select>
                </div>
              </div>

              <!-- Text Input -->
              <div v-if="inputType === 'text'" class="mt-6">
                <label for="identifiers" class="block text-sm font-medium text-gray-700">
                  Identifiers (one per line)
                </label>
                <textarea
                  id="identifiers"
                  v-model="textInput"
                  rows="4"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  placeholder="Enter your identifiers..."
                ></textarea>
              </div>

              <!-- File Upload -->
              <div v-else class="mt-6">
                <label class="block text-sm font-medium text-gray-700">File Upload</label>
                <div class="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md">
                  <div class="space-y-1 text-center">
                    <svg
                      class="mx-auto h-12 w-12 text-gray-400"
                      stroke="currentColor"
                      fill="none"
                      viewBox="0 0 48 48"
                      aria-hidden="true"
                    >
                      <path
                        d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                      />
                    </svg>
                    <div class="flex text-sm text-gray-600">
                      <label
                        for="file-upload"
                        class="relative cursor-pointer rounded-md font-medium text-indigo-600 hover:text-indigo-500"
                      >
                        <span>Upload a file</span>
                        <input 
                          id="file-upload" 
                          type="file" 
                          class="sr-only"
                          @change="handleFileUpload"
                          accept=".txt,.csv"
                        >
                      </label>
                      <p class="pl-1">or drag and drop</p>
                    </div>
                    <p class="text-xs text-gray-500">CSV or TXT up to 10MB</p>
                  </div>
                </div>
              </div>

              <!-- Database Selection -->
              <div class="mt-6">
                <h3 class="text-sm font-medium text-gray-700">Select Databases</h3>
                <div class="mt-4 space-y-4">
                  <div class="flex items-start" v-for="db in databases" :key="db.id">
                    <div class="flex items-center h-5">
                      <input
                        :id="db.id"
                        type="checkbox"
                        v-model="selectedDatabases"
                        :value="db.id"
                        class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                      >
                    </div>
                    <div class="ml-3 text-sm">
                      <label :for="db.id" class="font-medium text-gray-700">{{ db.name }}</label>
                      <p class="text-gray-500">{{ db.description }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <div class="mt-6">
                <button
                  type="submit"
                  :disabled="!isFormValid || loading"
                  class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                  {{ loading ? 'Processing...' : 'Submit Query' }}
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
import { ref, computed } from 'vue'

const inputType = ref('text')
const identifierType = ref('gene')
const textInput = ref('')
const selectedFile = ref(null)
const selectedDatabases = ref([])
const loading = ref(false)

const databases = [
  {
    id: 'disgenet',
    name: 'DisGeNET',
    description: 'Database of gene-disease associations'
  },
  {
    id: 'string',
    name: 'STRING',
    description: 'Protein-protein interaction network'
  },
  {
    id: 'reactome',
    name: 'Reactome',
    description: 'Pathway database'
  }
]

const isFormValid = computed(() => {
  if (selectedDatabases.value.length === 0) return false
  if (inputType.value === 'text' && !textInput.value.trim()) return false
  if (inputType.value === 'file' && !selectedFile.value) return false
  return true
})

function handleFileUpload(event) {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 10 * 1024 * 1024) {
      alert('File size must be less than 10MB')
      event.target.value = ''
      return
    }
    selectedFile.value = file
  }
}

async function submitQuery() {
  if (!isFormValid.value) return
  
  loading.value = true
  try {
    // TODO: Implement query submission
    console.log('Submitting query:', {
      inputType: inputType.value,
      identifierType: identifierType.value,
      textInput: textInput.value,
      selectedFile: selectedFile.value,
      selectedDatabases: selectedDatabases.value
    })
  } catch (error) {
    console.error('Error submitting query:', error)
  } finally {
    loading.value = false
  }
}
</script>