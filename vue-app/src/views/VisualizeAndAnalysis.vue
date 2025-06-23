<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Header Section with Title -->
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
          Graph Visualization and Analysis
        </h1>
        <p class="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
          View and manage data visualization and analysis.
        </p>
      </div>

      <!-- Tab Buttons with Sticky Blue Header -->
      <div class="mt-12 bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-800 px-6 py-4">
          <div class="flex space-x-8">
            <!-- Graph Visualization Tab Button -->
            <button
              @click="selectedTab = 'visualization'"
              :class="{
                'text-white border-b-2 border-indigo-400': selectedTab === 'visualization',
                'text-indigo-200': selectedTab !== 'visualization'
              }"
              class="pb-2 text-xl font-medium focus:outline-none"
            >
              <h2 class="text-xl font-semibold text-white">Graph Visualization</h2>
            </button>

            <!-- Graph Analysis Tab Button -->
            <button
              @click="selectedTab = 'analysis'"
              :class="{
                'text-white border-b-2 border-indigo-400': selectedTab === 'analysis',
                'text-indigo-200': selectedTab !== 'analysis'
              }"
              class="pb-2 text-xl font-medium focus:outline-none"
            >
              <h2 class="text-xl font-semibold text-white">Graph Analysis</h2>
            </button>
          </div>
        </div>
      </div>

      <!-- Tab Descriptions Below Titles -->
      <div class="from-indigo-600 to-indigo-800 px-6 py-4">
        <p v-if="selectedTab === 'visualization'" class="mt-1 text-black text-xl">
          Choose a tool for visualizing graph data. You can select Neo4j, Cytoscape, or GraphDb to view interactions, pathways, or networks in different formats.
        </p>

        <p v-if="selectedTab === 'analysis'" class="mt-1 text-black text-xl">
          Perform various analyses on your graph data. You can generate bar plots, pie charts, or interactive Plotly charts to explore your data visually.
        </p>
      </div>

      <!-- File Upload Section for Different Files -->
      <div v-if="!isFromQueryStep" class="mt-6 px-6 py-4 bg-white rounded-b-xl shadow-lg">
        <h3 class="text-xl font-semibold text-gray-900">Upload Data Files (Optional)</h3>

        <!-- Upload Combined Data -->
        <div class="mt-4">
          <button 
            @click="triggerFileInput('combined_df')"
            class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400"
            :disabled="isFromQueryStep"
          >
            Upload combined dataframe with all annotations (combined_df.tsv)
          </button>
          <input 
            ref="combinedFileInput"
            type="file"
            @change="handleFileUpload('combined_df')"
            class="hidden"
            accept=".tsv"
            data-type="combined_df"
          />
        </div>

        <!-- Upload combined_metadata -->
        <div class="mt-4">
          <button 
            @click="triggerFileInput('combined_metadata')"
            class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400"
            :disabled="isFromQueryStep"
          >
            Upload combined metadata (combined_metadata.json)
          </button>
          <input 
            ref="combinedMetadataFileInput"
            type="file"
            @change="handleFileUpload('combined_metadata')"
            class="hidden"
            accept=".json"
            data-type="combined_metadata"
          />
        </div>

        <!-- Upload OpenTargets Data -->
        <div class="mt-4">
          <button 
            @click="triggerFileInput('opentargets_df')"
            class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400"
            :disabled="isFromQueryStep"
          >
            Upload disease annotations for compounds dataframe from the OpenTargets (opentargets_df.tsv)
          </button>
          <input 
            ref="opentargetsFileInput"
            type="file"
            @change="handleFileUpload('opentargets_df')"
            class="hidden"
            accept=".tsv"
            data-type="opentargets_df"
          />
        </div>
      </div>

      <!-- Tab Content Area -->
      <div class="mt-6">
        <!-- Graph Visualization Tab Content -->
        <div v-if="selectedTab === 'visualization'" class="px-6 py-4 bg-white rounded-b-xl shadow-lg">
          <h3 class="text-xl font-semibold text-gray-900">Select Graph Visualization Tool</h3>
          <div class="mt-4">
            <select v-model="selectedVisualizationTool" class="block w-full rounded-lg border-gray-300 shadow-sm focus:ring-2 focus:ring-indigo-500 focus:outline-none p-3 text-lg bg-white hover:bg-indigo-50">
              <option value="neo4j">Neo4j</option>
              <option value="cytoscape">Cytoscape</option>
              <option value="graphdb">GraphDb</option>
            </select>
          </div>

          <!-- Tool Descriptions -->
          <div class="mt-4 text-xl text-gray-600">
            <div v-if="selectedVisualizationTool === 'neo4j'">
              <p>A powerful graph database for storing and visualizing complex relationships within data using graph structures.</p>
            </div>
            <div v-if="selectedVisualizationTool === 'cytoscape'">
              <p>A visualization tool designed for analyzing molecular interaction networks and biological data.</p>
            </div>
            <div v-if="selectedVisualizationTool === 'graphdb'">
              <p>A graph database optimized for storing and querying large-scale graph data.</p>
            </div>
          </div>
          <!-- Conditional Button for Neo4j -->
          <div v-if="selectedVisualizationTool === 'neo4j'">
            <button
              type="button"
              @click="continueToVisualize"
              class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
            >
              Continue to visualize in Neo4j
              <ArrowRightIcon class="ml-2 -mr-0.5 h-4 w-4" aria-hidden="true" />
            </button>
          </div>

        </div>

        <!-- Graph Analysis Tab Content -->
        <div v-if="selectedTab === 'analysis'" class="px-6 py-4 bg-white rounded-b-xl shadow-lg">
          <h3 class="text-xl font-semibold text-gray-900">Graph Analysis</h3>
          <div class="mt-4">
            <button @click="runGraphAnalysis('barplot')" class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400">
              Plot Bar Plot
            </button>
            <button @click="runGraphAnalysis('piechart')" class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400">
              Plot Pie Chart
            </button>
            <button @click="runGraphAnalysis('plotly')" class="inline-flex items-center border-2 border-dashed border-gray-500 px-4 py-2 text-sm font-semibold text-gray-700 rounded-lg hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-400">
              Plot Plotly Chart
            </button>
          </div>
        </div>
      </div>

      <!-- Footer Actions -->
      <div class="mt-8 flex justify-between px-6 py-4 bg-white rounded-b-xl shadow-lg">
        <button
          type="button"
          @click="goBack"
          class="rounded-md bg-white px-3 py-2 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50"
        >
          Go back to query building step
        </button>
        <button
          type="button"
          @click="continueToAnalysis"
          class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        >
          Continue to Visualize and Analysis
          <ArrowRightIcon class="ml-2 -mr-0.5 h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ArrowRightIcon } from '@heroicons/vue/24/outline'
import { useRouter } from 'vue-router'

const router = useRouter()

// The active tab is stored in the selectedTab variable
const selectedTab = ref('visualization')  // Default tab is 'visualization'
const selectedVisualizationTool = ref('neo4j')  // Default tool is Neo4j
// Watch for changes to selectedVisualizationTool to ensure the description updates
watch(selectedVisualizationTool, (newValue) => {
  console.log('Selected tool:', newValue)
})

// Flag to check if user came from the Query Step
const isFromQueryStep = ref(false) // This flag will be set to true when user clicks Continue to Visualize and Analysis

// For the file uploads
const handleFileUpload = (fileType) => (event) => {
  if (isFromQueryStep.value) return; // Do not allow upload if the user is in the visualization/analysis flow

  const file = event.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      console.log(`Uploaded ${fileType} file content:`, reader.result)
    }
    reader.readAsText(file)
  }
}

// Triggering file input by type
const triggerFileInput = (fileType) => {
  const fileInput = document.querySelector(`input[type="file"][data-type="${fileType}"]`)
  if (fileInput) fileInput.click()
}

function goBack() {
  console.log("Going back to the previous step.")
  router.push('/query')
}

function continueToAnalysis() {
  isFromQueryStep.value = true;
  console.log("Continuing to visualize and analysis.")
  // Proceed to visualization and analysis steps
}
</script>
