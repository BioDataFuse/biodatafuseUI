<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 sm:px-0">
      <h2 class="text-2xl font-semibold text-gray-900">Analysis Dashboard</h2>
      <p class="mt-1 text-sm text-gray-600">
        View and manage your data analysis tasks.
      </p>
    </div>

    <div class="mt-6">
      <div class="bg-white shadow overflow-hidden sm:rounded-lg">
        <!-- Analysis Stats -->
        <div class="px-4 py-5 sm:p-6">
          <dl class="grid grid-cols-1 gap-5 sm:grid-cols-3">
            <div class="px-4 py-5 bg-white shadow rounded-lg overflow-hidden sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">
                Total Analyses
              </dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">
                {{ stats.total }}
              </dd>
            </div>
            <div class="px-4 py-5 bg-white shadow rounded-lg overflow-hidden sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">
                Running
              </dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">
                {{ stats.running }}
              </dd>
            </div>
            <div class="px-4 py-5 bg-white shadow rounded-lg overflow-hidden sm:p-6">
              <dt class="text-sm font-medium text-gray-500 truncate">
                Completed
              </dt>
              <dd class="mt-1 text-3xl font-semibold text-gray-900">
                {{ stats.completed }}
              </dd>
            </div>
          </dl>
        </div>

        <!-- Analysis List -->
        <div class="px-4 sm:px-6 lg:px-8">
          <div class="mt-8 flex flex-col">
            <div class="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
              <div class="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
                <div class="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
                  <table class="min-w-full divide-y divide-gray-300">
                    <thead class="bg-gray-50">
                      <tr>
                        <th scope="col" class="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 sm:pl-6">
                          Analysis Name
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                          Status
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                          Created
                        </th>
                        <th scope="col" class="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">
                          Progress
                        </th>
                        <th scope="col" class="relative py-3.5 pl-3 pr-4 sm:pr-6">
                          <span class="sr-only">Actions</span>
                        </th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200 bg-white">
                      <tr v-for="analysis in analyses" :key="analysis.id">
                        <td class="whitespace-nowrap py-4 pl-4 pr-3 text-sm font-medium text-gray-900 sm:pl-6">
                          {{ analysis.name }}
                        </td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                          <span :class="{
                            'px-2 inline-flex text-xs leading-5 font-semibold rounded-full': true,
                            'bg-green-100 text-green-800': analysis.status === 'completed',
                            'bg-yellow-100 text-yellow-800': analysis.status === 'running',
                            'bg-gray-100 text-gray-800': analysis.status === 'pending'
                          }">
                            {{ analysis.status }}
                          </span>
                        </td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                          {{ analysis.created }}
                        </td>
                        <td class="whitespace-nowrap px-3 py-4 text-sm text-gray-500">
                          <div class="w-full bg-gray-200 rounded-full h-2.5">
                            <div 
                              class="bg-indigo-600 h-2.5 rounded-full" 
                              :style="{ width: `${analysis.progress}%` }"
                            ></div>
                          </div>
                        </td>
                        <td class="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                          <button
                            @click="viewAnalysis(analysis)"
                            class="text-indigo-600 hover:text-indigo-900"
                          >
                            View
                          </button>
                          <button
                            v-if="analysis.status === 'running'"
                            @click="stopAnalysis(analysis)"
                            class="ml-4 text-red-600 hover:text-red-900"
                          >
                            Stop
                          </button>
                          <button
                            v-if="analysis.status === 'completed'"
                            @click="downloadResults(analysis)"
                            class="ml-4 text-green-600 hover:text-green-900"
                          >
                            Download
                          </button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Analysis Details Modal -->
    <TransitionRoot appear :show="isModalOpen" as="template">
      <Dialog as="div" class="relative z-10" @close="closeModal">
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0"
          enter-to="opacity-100"
          leave="ease-in duration-200"
          leave-from="opacity-100"
          leave-to="opacity-0"
        >
          <div class="fixed inset-0 bg-black bg-opacity-25" />
        </TransitionChild>

        <div class="fixed inset-0 overflow-y-auto">
          <div class="flex min-h-full items-center justify-center p-4 text-center">
            <TransitionChild
              as="template"
              enter="ease-out duration-300"
              enter-from="opacity-0 scale-95"
              enter-to="opacity-100 scale-100"
              leave="ease-in duration-200"
              leave-from="opacity-100 scale-100"
              leave-to="opacity-0 scale-95"
            >
              <DialogPanel class="w-full max-w-2xl transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                <DialogTitle as="h3" class="text-lg font-medium leading-6 text-gray-900">
                  Analysis Details
                </DialogTitle>
                <div class="mt-4">
                  <div v-if="selectedAnalysis" class="space-y-4">
                    <div>
                      <h4 class="text-sm font-medium text-gray-500">Name</h4>
                      <p class="mt-1">{{ selectedAnalysis.name }}</p>
                    </div>
                    <div>
                      <h4 class="text-sm font-medium text-gray-500">Description</h4>
                      <p class="mt-1">{{ selectedAnalysis.description }}</p>
                    </div>
                    <div>
                      <h4 class="text-sm font-medium text-gray-500">Parameters</h4>
                      <pre class="mt-1 whitespace-pre-wrap bg-gray-50 p-2 rounded">{{ JSON.stringify(selectedAnalysis.parameters, null, 2) }}</pre>
                    </div>
                    <div v-if="selectedAnalysis.results">
                      <h4 class="text-sm font-medium text-gray-500">Results</h4>
                      <div class="mt-1 bg-gray-50 p-4 rounded">
                        {{ selectedAnalysis.results }}
                      </div>
                    </div>
                  </div>
                </div>

                <div class="mt-6 flex justify-end space-x-3">
                  <button
                    type="button"
                    class="inline-flex justify-center rounded-md border border-transparent bg-indigo-100 px-4 py-2 text-sm font-medium text-indigo-900 hover:bg-indigo-200 focus:outline-none"
                    @click="closeModal"
                  >
                    Close
                  </button>
                </div>
              </DialogPanel>
            </TransitionChild>
          </div>
        </div>
      </Dialog>
    </TransitionRoot>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Dialog, DialogPanel, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'

// Stats data
const stats = ref({
  total: 0,
  running: 0,
  completed: 0
})

// Analysis list
const analyses = ref([])

// Modal state
const isModalOpen = ref(false)
const selectedAnalysis = ref(null)

// Load initial data
onMounted(async () => {
  try {
    // TODO: Replace with actual API call
    analyses.value = [
      {
        id: 1,
        name: 'Gene Expression Analysis',
        status: 'completed',
        created: '2024-01-30',
        progress: 100,
        description: 'Analysis of differential gene expression in cancer samples',
        parameters: {
          datasetId: 'GSE123456',
          threshold: 0.05,
          foldChange: 2
        },
        results: 'Found 150 differentially expressed genes'
      },
      {
        id: 2,
        name: 'Pathway Analysis',
        status: 'running',
        created: '2024-01-31',
        progress: 65,
        description: 'Pathway enrichment analysis of selected genes',
        parameters: {
          geneList: ['BRCA1', 'TP53', 'EGFR'],
          database: 'KEGG'
        }
      }
    ]

    // Update stats
    stats.value = {
      total: analyses.value.length,
      running: analyses.value.filter(a => a.status === 'running').length,
      completed: analyses.value.filter(a => a.status === 'completed').length
    }
  } catch (error) {
    console.error('Error loading analyses:', error)
  }
})

// Actions
function viewAnalysis(analysis) {
  selectedAnalysis.value = analysis
  isModalOpen.value = true
}

function closeModal() {
  isModalOpen.value = false
  selectedAnalysis.value = null
}

async function stopAnalysis(analysis) {
  try {
    // TODO: Implement stop analysis API call
    console.log('Stopping analysis:', analysis.id)
  } catch (error) {
    console.error('Error stopping analysis:', error)
  }
}

async function downloadResults(analysis) {
  try {
    // TODO: Implement download results API call
    console.log('Downloading results for analysis:', analysis.id)
  } catch (error) {
    console.error('Error downloading results:', error)
  }
}
</script>