<template>
  <div class="bg-white py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Package Overview -->
      <h2 class="text-3xl font-extrabold text-gray-900 mb-4">Package Overview & Installation</h2>
      <p class="text-lg text-gray-600 mb-4 max-w-3xl">
        For detailed installation instructions, API references, and usage guidelines, please refer to our official documentation:
      </p>
      <a
        href="https://pybiodatafuse.readthedocs.io/en/latest/index.html"
        class="text-indigo-600 hover:underline text-lg"
        target="_blank"
      >
        https://pybiodatafuse.readthedocs.io/en/latest/
      </a>

      <!-- Data Sources Section -->
      <h2 class="text-2xl font-bold text-gray-800 mt-16 mb-4">Supported Data Sources</h2>
      <p class="text-gray-600 mb-6">
        BioDataFuse integrates data from multiple biological databases. Below is a list of currently supported data sources with their version and endpoint information.
      </p>

      <div v-if="loadingMetadata" class="text-gray-500 text-sm">Loading data sources...</div>
      <div v-else-if="metadataError" class="text-red-500 text-sm">{{ metadataError }}</div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="source in datasourceMetadata"
          :key="source.id"
          class="bg-gray-50 rounded-lg p-4 shadow border border-gray-200"
        >
          <h4 class="text-lg font-semibold text-indigo-700">{{ source.name }}</h4>
          <p class="text-gray-600 text-sm mt-1">{{ source.description }}</p>
          <p class="text-xs text-gray-400 mt-2">
            <span v-if="source.version && source.version !== 'unknown'">Version: {{ source.version }}</span>
            <span v-if="source.version && source.version !== 'unknown' && source.endpoint"> · </span>
            <span v-if="source.endpoint">
              Endpoint: <a :href="source.endpoint" target="_blank" rel="noopener noreferrer" class="hover:text-indigo-500 break-all">{{ source.endpoint }}</a>
            </span>
          </p>
        </div>
      </div>

      <!-- Notebook Section Title -->
      <h2 class="text-2xl font-bold text-gray-800 mt-16 mb-4">Example Workflows & Notebooks</h2>
      <p class="text-gray-600 mb-6">
        The following Jupyter notebooks demonstrate real-world applications of <code>pyBiodatafuse</code> for various biological data integration tasks.
      </p>

      <!-- Gene-to-Graph Workflow -->
      <div class="bg-gray-50 rounded-lg p-6 shadow mt-12">
        <h3 class="text-xl font-semibold text-indigo-700 mb-2">Gene-to-Graph Workflow Notebook</h3>
        <p class="text-gray-700 mb-4">
          This notebook walks through generating a context-specific knowledge graph from a list of gene identifiers.
        </p>

        <button
          @click="showGeneSteps = !showGeneSteps"
          class="mb-4 inline-flex items-center text-indigo-600 font-medium hover:underline focus:outline-none"
        >
          {{ showGeneSteps ? 'Hide Details ▲' : 'Show Workflow Steps ▼' }}
        </button>
        <br>  

        <Transition name="fade">
          <ul v-if="showGeneSteps" class="list-disc list-inside text-gray-700 space-y-1 ml-4">
            <li>Entity resolution with BridgeDB</li>
            <li>Functional annotations (expression, pathways, GO terms)</li>
            <li>Disease and compound associations</li>
            <li>Protein-protein interactions (STRING)</li>
            <li>Graph generation and serialization</li>
            <li>Export options: RDF (ttl), Cytoscape, Neo4j, GraphDB</li>
            <li>SHACL and ShEx shape generation for semantic validation</li>
          </ul>
        </Transition>

        <a
          href="https://github.com/BioDataFuse/pyBiodatafuse/blob/main/examples/01_gene_to_graph_workflow.ipynb"
          target="_blank"
          class="mt-4 inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          View Notebook on GitHub
        </a>
      </div>

      <!-- Metabolite Workflow -->
      <div class="bg-gray-50 rounded-lg p-6 shadow mt-12">
        <h3 class="text-xl font-semibold text-indigo-700 mb-2">Metabolite Workflow Notebook</h3>
        <p class="text-gray-700 mb-4">
          This notebook demonstrates how to generate a knowledge graph from a list of metabolites or compounds.
        </p>

        <button
          @click="showMetaboliteSteps = !showMetaboliteSteps"
          class="mb-4 inline-flex items-center text-indigo-600 font-medium hover:underline focus:outline-none"
        >
          {{ showMetaboliteSteps ? 'Hide Details ▲' : 'Show Workflow Steps ▼' }}
        </button>
        <br>  

        <Transition name="fade">
          <ul v-if="showMetaboliteSteps" class="list-disc list-inside text-gray-700 space-y-1 ml-4">
            <li>Entity resolution using BridgeDB</li>
            <li>Transporter inhibitor annotations from MolMeDB</li>
            <li>Disease associations from OpenTargets</li>
            <li>Graph creation and metadata integration</li>
            <li>Graph export in multiple formats</li>
            <li>Visual summaries using BioGraph analysis</li>
          </ul>
        </Transition>

        <a
          href="https://github.com/BioDataFuse/pyBiodatafuse/blob/main/examples/02_metabolite_to_graph.ipynb"
          target="_blank"
          class="mt-4 inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          View Notebook on GitHub
        </a>
      </div>

      <!-- DEG Workflow -->
      <div class="bg-gray-50 rounded-lg p-6 shadow mt-12">
        <h3 class="text-xl font-semibold text-indigo-700 mb-2">DEG Analysis Workflow Notebook</h3>
        <p class="text-gray-700 mb-4">
          This notebook demonstrates how to build a graph from a file containing differentially expressed genes (DEGs),
          typically from transcriptomics experiments.
        </p>

        <button
          @click="showDEGSteps = !showDEGSteps"
          class="mb-4 inline-flex items-center text-indigo-600 font-medium hover:underline focus:outline-none"
        >
          {{ showDEGSteps ? 'Hide Details ▲' : 'Show Workflow Steps ▼' }}
        </button>
        <br>  

        <Transition name="fade">
          <ul v-if="showDEGSteps" class="list-disc list-inside text-gray-700 space-y-1 ml-4">
            <li>Loading and filtering a DEA result table</li>
            <li>Gene entity resolution via BridgeDB</li>
            <li>KEGG pathway annotations</li>
            <li>Transporter-inhibitor mappings from MolMeDB</li>
            <li>Combining annotations and building a BDF graph</li>
            <li>Basic statistics and visual summaries with <code>BioGraph</code></li>
          </ul>
        </Transition>

        <a
          href="https://github.com/BioDataFuse/pyBiodatafuse/blob/main/examples/dea_workflow.ipynb"
          target="_blank"
          class="mt-4 inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          View Notebook on GitHub
        </a>
      </div>

      <!-- PCS Workflow Section -->
      <div class="bg-gray-50 rounded-lg p-6 shadow mt-12">
        <h3 class="text-xl font-semibold text-indigo-700 mb-2">
          Post-COVID Syndrome (PCS) Workflow Notebook
        </h3>
        <p class="text-gray-700 mb-4">
          This advanced use case demonstrates how to construct a knowledge graph for Post-COVID Syndrome (PCS),
          integrating multi-source biological data and enabling downstream RDF and graph database exports.
        </p>

        <button
          @click="showPCSSteps = !showPCSSteps"
          class="mb-4 inline-flex items-center text-indigo-600 font-medium hover:underline focus:outline-none"
        >
          {{ showPCSSteps ? 'Hide Details ▲' : 'Show Workflow Steps ▼' }}
        </button>
        <br>  

        <Transition name="fade">
          <ul v-if="showPCSSteps" class="list-disc list-inside text-gray-700 space-y-1 ml-4">
            <li>Gene entity resolution via BridgeDB</li>
            <li>Gene-disease associations via DisGeNET and literature curation</li>
            <li>Disease-compound and gene-compound interactions via OpenTargets</li>
            <li>Pathway annotations from MINERVA and Reactome</li>
            <li>Gene ontology enrichment and PPI data from StringDB</li>
            <li>Comprehensive KG generation and export to Neo4j, Cytoscape, and RDF</li>
            <li>SHACL and ShEx schema generation using shexer</li>
          </ul>
        </Transition>

        <router-link
          to="https://github.com/BioDataFuse/pyBiodatafuse/blob/main/examples/usecases/PCS/PCS.ipynb"
          target="_blank"
          class="mt-4 inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          View Notebook on GitHub
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const showGeneSteps = ref(false)
const showMetaboliteSteps = ref(false)
const showDEGSteps = ref(false)
const showPCSSteps = ref(false)

// Data sources metadata
const datasourceMetadata = ref([])
const loadingMetadata = ref(true)
const metadataError = ref(null)

onMounted(async () => {
  try {
    const response = await axios.get('/api/datasources/metadata')
    datasourceMetadata.value = response.data
  } catch (err) {
    metadataError.value = 'Failed to load data source metadata'
    console.error('Error fetching metadata:', err)
  } finally {
    loadingMetadata.value = false
  }
})
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
.fade-enter-to, .fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}
</style>
