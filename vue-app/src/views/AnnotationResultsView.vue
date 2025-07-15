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
          <h2 class="text-xl font-semibold text-white">Step 3: Annotation Results</h2>
          <p class="mt-1 text-indigo-200">Review the annotation results before continuing to visualization.</p>
          <p class="mt-1 text-indigo-200">
            <strong>Note: </strong> You can go back to the previous step to modify your query.
          </p>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="mt-4 text-center">
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
              <div v-if="annotationResults?.captured_warnings?.length" class="bg-gray-200 p-4 mb-4 rounded-md">
                <div class="text-sm text-gray-700">
                  <strong class="font-semibold text-gray-900">Warnings:</strong>
                  <ul class="list-disc pl-5 space-y-2 mt-1">
                    <li v-for="(warning, index) in annotationResults?.captured_warnings" :key="index">
                      {{ warning }}
                    </li>
                  </ul>
                </div>
              </div>
              <!-- Annotation Results Table -->
              <!-- Filter Controls -->
              <div class="mt-1 space-y-4">
                <div class="flex flex-col sm:flex-row sm:space-x-6 sm:items-end">
                  <!-- Select Input ID -->
                  <div class="w-full sm:w-1/2">
                    <label class="text-xl font-bold text-blue-900">Select Input</label>
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

              <!-- Table Display -->
              <div v-if="selectedDataSourceData.length" class="mt-6">
                <h3 class="text-lg font-semibold text-gray-900 mb-2 text-left">
                  Annotation results for 
                  <span class="underline font-bold">{{ selectedInputId }}</span> 
                  : {{ selectedDataSource }}
                </h3>

                <div class="overflow-x-auto">
                  <table class="min-w-full divide-y divide-gray-200 text-sm text-gray-700 border rounded">
                    <thead>
                      <tr>
                        <th
                          v-for="(v, key, i) in selectedDataSourceData[0]"
                          :key="`header-${key}-${i}`"
                          class="px-2 py-1 font-semibold border-b text-left bg-gray-50"
                        >
                          {{ key }}
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(entry, idx) in paginatedAnnotationData" :key="idx" class="border-t">
                        <td
                          v-for="(val, k) in entry"
                          :key="`cell-${idx}-${k}`"
                          class="px-2 py-1 border-b text-left"
                        >
                          {{ val }}
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <div class="mt-4 flex items-center space-x-4">
                  <button
                    @click="currentAnnotationPage--"
                    :disabled="currentAnnotationPage === 1"
                    class="px-3 py-1 text-sm text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50"
                  >
                    Previous
                  </button>
                  <span class="text-sm text-gray-500">
                    Page {{ currentAnnotationPage }} of {{ annotationTotalPages }}
                  </span>
                  <button
                    @click="currentAnnotationPage++"
                    :disabled="currentAnnotationPage === annotationTotalPages"
                    class="px-3 py-1 text-sm text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-100 disabled:opacity-50"
                  >
                    Next
                  </button>
                </div>
              </div>

              <!-- Download Buttons for combined_df and combined_metadata as TSV -->
              <div>
                <div class="mt-8 text-left">
                  <h3 class="text-xl font-semibold text-gray-900">Download outputs</h3>
                </div>
                <!-- Download combined_df TSV -->
                <div v-if="!isContinueDisabled" class="mt-4 flex justify-left space-x-2">
                  <button @click="downloadTSV('combined_df')" class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400">
                    <svg class="w-4 h-4 mr-2 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                    </svg>
                    Combined table with all annotations (TSV)
                  </button>
                </div>
                <!-- Download combined metadata JSON -->
                <div class="mt-1 flex justify-left space-x-2">
                  <button @click="downloadJSON('combined_metadata')" class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400">
                    <svg class="w-4 h-4 mr-2 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                    </svg>
                    Combined query metadata (JSON)
                  </button>
                </div>
                <!-- Download Button for opentargets_df TSV if it is not empty or None -->
                <div v-if="annotationResults?.opentargets_df && Object.keys(annotationResults.opentargets_df).length > 0" class="mt-1 flex justify-left space-x-2">
                  <button @click="downloadTSV('opentargets_df')" class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400">
                    <svg class="w-4 h-4 mr-2 text-gray-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                    </svg>
                    Download disease annotations for compounds dataframe from the OpenTargets (TSV)
                  </button>
                </div>

              </div>
              <!-- Navigation Actions -->
              <div class="mt-8 flex justify-between">
                <button
                  @click="goBack"
                  class="inline-flex items-center rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
                >
                  Back to Data Sources
                </button>
                <div class="flex flex-col items-end space-y-2">
                  <button
                    @click="continueToVisualizeAndAnalysis"
                    :disabled="isContinueDisabled"
                    class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm 
                          hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 
                          focus-visible:outline-indigo-600 disabled:opacity-50"
                  >
                    Continue to Visualize and Analysis
                    <ArrowRightIcon class="ml-2 -mr-0.5 h-4 w-4" aria-hidden="true" />
                  </button>
                </div>
              </div>
              <div> 
                <p v-if="isContinueDisabled" class="text-right text-sm text-red-600">
                  Cannot continue: No available annotations for any input. Please check your input or data source selections.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ExclamationCircleIcon, ArrowRightIcon } from '@heroicons/vue/24/outline'

const router = useRouter()
const loading = ref(true)
const error = ref(null)
const annotationResults = ref(null)
const currentAnnotationPage = ref(1)
const rowsPerAnnotationPage = 5

const steps = [
  { name: 'Input Identifiers', status: 'complete' },
  { name: 'Identifier Mapping', status: 'complete' },
  { name: 'Select Data Sources', status: 'complete' },
  { name: 'Annotations', status: 'current' },
]

const currentStep = ref(3)
const fixedFields = ["identifier", "identifier.source", "target", "target.source"]

const selectedInputId = ref('')
const selectedDataSource = ref('')

const availableInputIds = computed(() => {
  const allInputs = Object.values(annotationResults.value?.combined_df || {}).map(item => item.identifier);
  const uniqueInputs = [...new Set(allInputs)];
  return uniqueInputs;

});

const paginatedAnnotationData = computed(() => {
  const start = (currentAnnotationPage.value - 1) * rowsPerAnnotationPage
  const end = start + rowsPerAnnotationPage
  return selectedDataSourceData.value.slice(start, end)
})

const annotationTotalPages = computed(() => {
  return Math.ceil(selectedDataSourceData.value.length / rowsPerAnnotationPage)
})

const availableDataSources = computed(() => {
  const inputId = selectedInputId.value
  if (!inputId) return []

  const row = Object.values(annotationResults.value?.combined_df || {}).find(item => item.identifier === inputId)
  return Object.keys(row).filter(k => !fixedFields.includes(k) && Array.isArray(row[k]))
})

const allInputsHaveNoDataSources = computed(() => {
  const df = annotationResults.value?.combined_df
  if (!df) return true

  const allRows = Object.values(df)

  return allRows.every(row => {
    const dataSourceKeys = Object.keys(row).filter(
      k => !fixedFields.includes(k) && Array.isArray(row[k])
    )
    return dataSourceKeys.length === 0
  })
})


const selectedDataSourceData = computed(() => {
  if (!selectedInputId.value || !selectedDataSource.value) return []
  const selectedRow = Object.values(annotationResults.value?.combined_df || {}).find(item => item.identifier === selectedInputId.value)
  return selectedRow ? selectedRow[selectedDataSource.value] : []
})

watch(selectedInputId, (newInputId) => {
  // Reset the data source selection and annotation data when input ID changes
  selectedDataSource.value = ''; // Reset Data Source selection
  currentAnnotationPage.value = 1; // Reset to first page
  
  if (newInputId) {
    selectedDataSourceData.value = getSelectedDataSourceData(newInputId); // Get new data for the selected input
  } else {
    selectedDataSourceData.value = []; // Clear data if no valid input ID
  }
});

watch(selectedDataSource, (newDataSource) => {
  if (selectedInputId.value) {
    selectedDataSourceData.value = getSelectedDataSourceData(selectedInputId.value); // Update data based on selected input and source
  }
});

function getSelectedDataSourceData(inputId) {
  const selectedRow = Object.values(annotationResults.value?.combined_df || {}).find(item => item.identifier === inputId);
  return selectedRow ? selectedRow[selectedDataSource.value] : [];
}

// Function to download TSV (for combined_df)
function downloadTSV(type) {
  const data = type === 'combined_df' ? annotationResults.value.combined_df : annotationResults.value.opentargets_df;
  const tsv = convertToTSV(data);
  const blob = new Blob([tsv], { type: 'text/tsv' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${type}.tsv`;
  link.click();
}

// Function to convert an object into TSV format
function convertToTSV(obj) {
const array = Object.keys(obj).map(key => {
    const { key: _, ...rest } = obj[key];  
    return rest;
  });
  const headers = Object.keys(array[0] || {}).join('\t'); // Use tab for delimiter

  const rows = array.map(item => {
    return Object.values(item).map(value => {
      // 
      if (typeof value === 'object' && value !== null) {
        return JSON.stringify(value); 
      }
      return value;
    }).join('\t'); 
  });

  return [headers, ...rows].join('\n'); 
}

// 
function downloadJSON(type) {
  const data = type === 'combined_metadata' ? annotationResults.value.combined_metadata : {};
  const json = JSON.stringify(data, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${type}.json`;
  link.click();
}

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

const isContinueDisabled = computed(() => {
  return allInputsHaveNoDataSources.value
})


function continueToVisualizeAndAnalysis() {
  if (isContinueDisabled.value) {
    return;
  }
  localStorage.setItem('isFromQueryStep', 'true');
  router.push('/visualize&analysis')
}
</script>
