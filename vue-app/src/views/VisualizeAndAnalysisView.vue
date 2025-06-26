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

        <!-- Suggest Custom Analysis / GitHub Link -->
        <div class="mb-6 bg-gray-100 border border-gray-300 rounded-lg p-4 text-gray-700">
          <strong>Need help with advanced analysis?</strong><br>
          Is there a specific analysis or algorithm you'd like to apply on the generated knowledge graph?<br>
          Do you need help implementing it?<br>
          👉 
          <a
            href="https://github.com/BioDataFuse/pyBiodatafuse/issues/new?template=analysis-support-request.md"
            target="_blank"
            rel="noopener noreferrer"
            class="text-indigo-600 hover:underline"
          >
            Create an issue on GitHub
          </a> and let us know!
        </div>

        <p v-if="selectedTab === 'analysis'" class="mt-1 text-black text-xl">
          Perform various analyses on your graph data. You can generate bar plots, pie charts, or interactive Plotly charts to explore your data visually.
        </p>
      </div>

      <!-- File Upload Section for Different Files -->
      <div v-if="!isFromQueryStep" class="mt-6 px-6 py-4 bg-white rounded-b-xl shadow-lg">
        <h3 class="text-xl font-semibold text-gray-900">Upload Query Outputs (Optional)</h3>

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
        </div>

        <!-- Graph Analysis Tab Content -->
      <div v-if="selectedTab === 'analysis'" class="px-6 py-4 bg-white rounded-b-xl shadow-lg">
        <h3 class="text-xl font-semibold text-gray-900 mb-4">Patent Analysis</h3>
        <textarea
          v-model="chemicalInput"
          placeholder="Enter compound names, one per line (e.g., Glucose, Aspirin)"
          rows="4"
          class="w-full p-3 border rounded-lg mb-4"
        ></textarea>

        <button
          @click="submitPatentAnalysis"
          class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-500"
        >
          Analyze Patents
        </button>

        <div class="mt-6" v-if="analysisResults">
          <h4 class="text-lg font-bold mb-2">Results</h4>
          <div v-for="(records, cid) in analysisResults" :key="cid" class="mb-4 border p-4 rounded">
            <p><strong>CID:</strong> {{ cid }}</p>
            <ul>
              <li v-for="entry in records" :key="entry.label">
                {{ entry.label }}: {{ entry.value }}
              </li>
            </ul>
          </div>
        </div>

        <p v-if="analysisError" class="mt-4 text-red-600">{{ analysisError }}</p>
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
          @click="handleContinue"
          class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
        >
          {{ continueButtonText }}
          <ArrowRightIcon class="ml-2 -mr-0.5 h-4 w-4" aria-hidden="true" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
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

// Dynamically generate button label based on selected tab and tool
const continueButtonText = computed(() => {
  if (selectedTab.value === 'visualization') {
    switch (selectedVisualizationTool.value) {
      case 'neo4j':
        return 'Continue to visualize in Neo4j'
      case 'cytoscape':
        return 'Continue to visualize in Cytoscape'
      case 'graphdb':
        return 'Continue to visualize in GraphDb'
      default:
        return 'Continue to Visualize'
    }
  } else {
    return 'Continue to Analysis'
  }
})

// Unified handler for continue button
function handleContinue() {
  isFromQueryStep.value = true;
  if (selectedTab.value === 'visualization') {
    console.log(`Continuing to visualize using ${selectedVisualizationTool.value}`)
    // TODO: Add router.push, redirect or trigger logic for each visualization tool
    if (selectedVisualizationTool.value === 'neo4j') {
      router.push('/visualize&analysis/neo4j')
    } else if (selectedVisualizationTool.value === 'cytoscape') {
      router.push('/visualize&analysis/cytoscape')
    } else if (selectedVisualizationTool.value === 'graphdb') {
      router.push('/visualize&analysis/graphdb')
    }
  } else {
    console.log("Continuing to graph analysis")
    // TODO: Handle analysis step logic
  }
}

</script>
