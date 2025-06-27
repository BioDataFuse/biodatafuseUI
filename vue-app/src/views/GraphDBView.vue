<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Header Section -->
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
          GraphDB Integration
        </h1>
        <p class="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
          Generate RDF graphs and manage your GraphDB repositories
        </p>
      </div>

      <!-- Step Navigation Bar -->
      <div class="mt-12 bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-800 px-6 py-4">
          <div class="flex space-x-8">
            <!-- Step 1: RDF Generation Tab -->
            <button
              @click="activeStep = 'generation'"
              :class="{
                'text-white border-b-2 border-indigo-400': activeStep === 'generation',
                'text-indigo-200 hover:text-white': activeStep !== 'generation'
              }"
              class="pb-2 text-xl font-medium focus:outline-none transition-colors"
            >
              <h2 class="text-xl font-semibold">1. Generate RDF Graph</h2>
            </button>

            <!-- Step 2: Preview RDF Graph Tab -->
            <button
              @click="hasGeneratedData && (activeStep = 'preview')"
              :class="{
                'text-white border-b-2 border-indigo-400': activeStep === 'preview',
                'text-indigo-200 hover:text-white': activeStep !== 'preview' && hasGeneratedData,
                'text-indigo-300 cursor-not-allowed': !hasGeneratedData
              }"
              class="pb-2 text-xl font-medium focus:outline-none transition-colors"
              :disabled="!hasGeneratedData"
            >
              <h2 class="text-xl font-semibold">2. Preview RDF Graph</h2>
            </button>

            <!-- Step 3: GraphDB Management Tab -->
            <button
              @click="hasGeneratedData && (activeStep = 'management')"
              :class="{
                'text-white border-b-2 border-indigo-400': activeStep === 'management',
                'text-indigo-200 hover:text-white': activeStep !== 'management' && hasGeneratedData,
                'text-indigo-300 cursor-not-allowed': !hasGeneratedData
              }"
              class="pb-2 text-xl font-medium focus:outline-none transition-colors"
              :disabled="!hasGeneratedData"
            >
              <h2 class="text-xl font-semibold">3. GraphDB Management</h2>
            </button>
          </div>
        </div>

        <!-- Tab Descriptions -->
        <div class="px-6 py-4 bg-gray-50 border-b">
          <div v-if="activeStep === 'generation'">
            <p class="text-gray-600">Configure and generate your RDF graph from annotation data</p>
          </div>
          <div v-else-if="activeStep === 'preview'">
            <p class="text-gray-600">Preview and download your generated RDF graph files</p>
          </div>
          <div v-else-if="activeStep === 'management'">
            <p class="text-gray-600">Connect to GraphDB and manage your repositories</p>
          </div>
        </div>

        <!-- Tab Content Area -->
        <div class="bg-white">
          <!-- Step 1: RDF Generation Content -->
          <div v-if="activeStep === 'generation'" class="px-6 py-6">
            <!-- Form Fields -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <!-- Base URI -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Base URI *</label>
                <input
                  type="url"
                  v-model="formData.baseUri"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="https://biodatafuse.org/example/"
                  required
                />
              </div>
              
              <!-- Version IRI -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Version IRI *</label>
                <input
                  type="url"
                  v-model="formData.versionIri"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="https://biodatafuse.org/example/test.owl"
                  required
                />
              </div>
              
              <!-- Author Name -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Author Name *</label>
                <input
                  type="text"
                  v-model="formData.authorName"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="Your Name"
                  required
                />
              </div>
              
              <!-- Author Email -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Author Email *</label>
                <input
                  type="email"
                  v-model="formData.authorEmail"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="your.email@example.com"
                  required
                />
              </div>
              
              <!-- ORCID -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">ORCID *</label>
                <input
                  type="url"
                  v-model="formData.orcid"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="https://orcid.org/0000-0000-0000-0000"
                  required
                />
              </div>
              
              <!-- Graph Name -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Graph Name *</label>
                <input
                  type="text"
                  v-model="formData.graphName"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="my_graph"
                  required
                />
              </div>
            </div>

            <!-- SHACL Options -->
            <div class="bg-gray-50 p-4 rounded-md mb-6">
              <div class="flex items-center mb-4">
                <input
                  type="checkbox"
                  id="generateShacl"
                  v-model="formData.generateShacl"
                  class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <label for="generateShacl" class="ml-2 text-sm font-medium text-gray-700">
                  Generate SHACL shapes
                </label>
              </div>
              
              <div v-if="formData.generateShacl" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">SHACL Threshold</label>
                  <input
                    type="number"
                    v-model.number="formData.shaclThreshold"
                    step="0.001"
                    min="0"
                    max="1"
                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
                
                <div class="flex items-center">
                  <input
                    type="checkbox"
                    id="generateUml"
                    v-model="formData.generateUmlDiagram"
                    class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                  />
                  <label for="generateUml" class="ml-2 text-sm text-gray-700">
                    Generate UML diagram
                  </label>
                </div>
              </div>
            </div>

            <!-- Status Messages -->
            <div v-if="loading" class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
              <div class="flex items-center">
                <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500 mr-3"></div>
                <span class="text-blue-700">{{ loadingMessage }}</span>
              </div>
            </div>

            <div v-if="errorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
              <p class="text-red-700">{{ errorMessage }}</p>
            </div>

            <!-- Generate Button -->
            <div class="flex justify-between items-center">
              <button
                @click="generateRDF"
                :disabled="loading || !isFormValid"
                class="inline-flex items-center bg-indigo-600 text-white px-6 py-3 rounded-md hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium shadow focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all duration-200"
              >
                <span v-if="loading" class="animate-spin mr-2">🔄</span>
                <span>{{ loading ? 'Generating...' : 'Generate RDF Graph' }}</span>
              </button>

              <!-- Auto-advance to step 2 button -->
              <button
                v-if="hasGeneratedData"
                @click="activeStep = 'preview'"
                class="inline-flex items-center bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 font-medium shadow focus:outline-none focus:ring-2 focus:ring-gray-400 transition-all duration-200"
              >
                <span>Preview Generated Files</span>
                <svg class="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Step 2: Preview RDF Graph Content -->
          <div v-if="activeStep === 'preview' && hasGeneratedData" class="px-6 py-6">
            <!-- Success Message -->
            <div class="bg-green-50 border border-green-200 rounded-md p-4 mb-6">
              <div class="flex">
                <div class="flex-shrink-0">
                  <svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                </div>
                <div class="ml-3">
                  <h3 class="text-sm font-medium text-green-800">RDF Graph Generated Successfully!</h3>
                  <div class="mt-2 text-sm text-green-700">
                    <p>Graph "{{ generatedData.graph_name || 'RDF Graph' }}" has been created with {{ generatedData.generated_files.length }} file(s).</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Files Grid -->
            <div class="mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Generated Files</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div 
                  v-for="file in generatedData.generated_files" 
                  :key="file.id"
                  class="border-2 border-dashed border-gray-300 rounded-lg p-4 hover:border-gray-400 transition-colors"
                >
                  <div class="flex items-center justify-between">
                    <div class="flex-1">
                      <h4 class="font-medium text-gray-900">{{ file.name }}</h4>
                      <p class="text-sm text-gray-500">{{ file.type }}</p>
                      <p class="text-xs text-gray-400">{{ formatFileSize(file.size) }}</p>
                      <p class="text-xs text-gray-400" v-if="file.created_at">
                        {{ formatDate(file.created_at) }}
                      </p>
                    </div>
                    <button
                      @click="downloadFile(file)"
                      class="inline-flex items-center bg-indigo-600 text-white px-3 py-2 rounded-md hover:bg-indigo-700 text-sm ml-2 font-medium shadow focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all duration-200"
                    >
                      Download
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- UML Diagram Preview -->
            <div v-if="umlFile && umlImageUrl" class="mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">UML Diagram</h3>
              <div class="border rounded-lg overflow-hidden bg-white">
                <img 
                  :src="umlImageUrl" 
                  alt="UML Diagram" 
                  class="max-w-full h-auto"
                  @error="onImageError"
                />
              </div>
            </div>

            <!-- RDF Preview -->
            <div v-if="rdfContent" class="mb-6">
              <h3 class="text-lg font-medium text-gray-900 mb-4">RDF Content Preview</h3>
              <div class="border rounded-lg overflow-hidden">
                <pre class="bg-gray-50 p-4 text-sm overflow-x-auto max-h-96"><code>{{ rdfContent }}</code></pre>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex justify-between items-center">
              <div class="flex space-x-4">
                <button
                  @click="regenerateRdf"
                  class="inline-flex items-center bg-gray-600 text-white px-4 py-2 rounded-md hover:bg-gray-700 font-medium shadow focus:outline-none focus:ring-2 focus:ring-gray-400 transition-all duration-200"
                >
                  Generate New RDF
                </button>
                <button
                  @click="downloadAllFiles"
                  class="inline-flex items-center bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 font-medium shadow focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-200"
                >
                  Download All Files
                </button>
              </div>
              
              <!-- Navigation to GraphDB Management -->
              <button
                @click="activeStep = 'management'"
                class="inline-flex items-center bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 font-medium shadow focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all duration-200"
              >
                <span>Continue to GraphDB Management</span>
                <svg class="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </div>

          <!-- Step 3: GraphDB Management Content -->
          <div v-if="activeStep === 'management' && hasGeneratedData" class="px-6 py-6">
            <!-- Instructions -->
            <div class="mb-6 bg-gray-50 border border-gray-200 rounded-md p-4">
              <p class="text-gray-700 text-sm">
                <strong>Instructions:</strong><br><br>
                • Ensure your <strong>GraphDB instance</strong> is running and accessible.<br>
                • Provide the correct base URL (e.g., http://localhost:7200).<br>
                • Username and password are optional if authentication is not required.<br>
                • Test your connection before uploading data.<br>
                • Make sure you have created or selected a repository.
              </p>
            </div>

            <!-- Status/Error Messages -->
            <div v-if="graphdbLoading" class="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-md">
              <div class="flex items-center">
                <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500 mr-3"></div>
                <span class="text-blue-700">{{ graphdbLoadingMessage }}</span>
              </div>
            </div>
            <div v-if="graphdbStatusMessage" class="mb-6 p-4 bg-green-50 border border-green-200 rounded-md">
              <p class="text-green-700">{{ graphdbStatusMessage }}</p>
            </div>
            <div v-if="graphdbErrorMessage" class="mb-6 p-4 bg-red-50 border border-red-200 rounded-md">
              <p class="text-red-700">{{ graphdbErrorMessage }}</p>
            </div>

            <!-- GraphDB Connection Form -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">GraphDB Base URL *</label>
                <input
                  type="url"
                  v-model="graphdbConfig.baseUrl"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="http://localhost:7200"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Repository Name</label>
                <input
                  type="text"
                  v-model="graphdbConfig.repositoryName"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  placeholder="my-repository"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Username (optional)</label>
                <input
                  type="text"
                  v-model="graphdbConfig.username"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Password (optional)</label>
                <input
                  type="password"
                  v-model="graphdbConfig.password"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex flex-wrap gap-4 mb-6">
              <button
                @click="testGraphDBConnection"
                :disabled="graphdbLoading || !graphdbConfig.baseUrl"
                class="inline-flex items-center bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 font-medium shadow focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-200"
              >
                <span v-if="graphdbLoading && graphdbLoadingMessage.includes('Testing')" class="animate-spin mr-2">🔄</span>
                <span>Test Connection</span>
              </button>
              <button
                @click="listRepositories"
                :disabled="graphdbLoading || !graphdbConfig.baseUrl"
                class="inline-flex items-center bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:opacity-50 font-medium shadow focus:outline-none focus:ring-2 focus:ring-indigo-400 transition-all duration-200"
              >
                <span v-if="graphdbLoading && graphdbLoadingMessage.includes('Fetching')" class="animate-spin mr-2">🔄</span>
                <span>List Repositories</span>
              </button>
              <button
                @click="createRepository"
                :disabled="graphdbLoading || !graphdbConfig.baseUrl || !graphdbConfig.repositoryName"
                class="inline-flex items-center bg-purple-600 text-white px-4 py-2 rounded-md hover:bg-purple-700 disabled:opacity-50 font-medium shadow focus:outline-none focus:ring-2 focus:ring-purple-400 transition-all duration-200"
              >
                <span v-if="graphdbLoading && graphdbLoadingMessage.includes('Creating')" class="animate-spin mr-2">🔄</span>
                <span>Create Repository</span>
              </button>
              <button
                @click="uploadRDFGraph"
                :disabled="graphdbLoading || !graphdbConfig.baseUrl || !graphdbConfig.repositoryName"
                class="inline-flex items-center bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 disabled:opacity-50 font-medium shadow focus:outline-none focus:ring-2 focus:ring-green-400 transition-all duration-200"
              >
                <span v-if="graphdbLoading && graphdbLoadingMessage.includes('Uploading')" class="animate-spin mr-2">🔄</span>
                <span>Upload RDF Graph</span>
              </button>
            </div>

            <!-- Repository List -->
            <div v-if="repositories.length > 0" class="mt-8">
              <h3 class="text-lg font-medium text-gray-900 mb-4">Available Repositories</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div 
                  v-for="repo in repositories" 
                  :key="repo.id"
                  class="border rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                  :class="{ 'border-indigo-500 bg-indigo-50': graphdbConfig.repositoryName === repo.id }"
                  @click="selectRepository(repo.id)"
                >
                  <h4 class="font-medium text-gray-900">{{ repo.id }}</h4>
                  <p class="text-sm text-gray-500">{{ repo.title || 'No title' }}</p>
                  <p class="text-xs text-gray-400 mt-1">Type: {{ repo.type || 'Unknown' }}</p>
                  <div class="mt-2 flex items-center text-xs">
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium mr-2"
                          :class="repo.readable ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                      {{ repo.readable ? 'Readable' : 'Not Readable' }}
                    </span>
                    <span class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                          :class="repo.writable ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                      {{ repo.writable ? 'Writable' : 'Read Only' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Repository Actions -->
            <div v-if="graphdbConfig.repositoryName" class="mt-6 p-4 bg-gray-50 rounded-md">
              <h4 class="font-medium text-gray-900 mb-3">Repository Actions: {{ graphdbConfig.repositoryName }}</h4>
              <div class="flex flex-wrap gap-3">
                <button
                  @click="countTriples"
                  :disabled="graphdbLoading"
                  class="inline-flex items-center bg-blue-600 text-white px-3 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50 text-sm font-medium shadow focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all duration-200"
                >
                  <span v-if="graphdbLoading && graphdbLoadingMessage.includes('Counting')" class="animate-spin mr-2">🔄</span>
                  <span>Count Triples</span>
                </button>
                <button
                  @click="deleteRepository"
                  :disabled="graphdbLoading"
                  class="inline-flex items-center bg-red-600 text-white px-3 py-2 rounded-md hover:bg-red-700 disabled:opacity-50 text-sm font-medium shadow focus:outline-none focus:ring-2 focus:ring-red-400 transition-all duration-200"
                >
                  <span v-if="graphdbLoading && graphdbLoadingMessage.includes('Deleting')" class="animate-spin mr-2">🔄</span>
                  <span>Delete Repository</span>
                </button>
              </div>
            </div>

            <!-- Navigation Actions -->
            <div class="mt-8 pt-6 border-t border-gray-200 flex justify-between">
              <button
                @click="activeStep = 'preview'"
                class="inline-flex items-center text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md hover:bg-gray-100 transition-all duration-200"
              >
                <svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                </svg>
                <span class="text-sm">Back to Preview</span>
              </button>
            </div>
          </div>

          <!-- Step 2 & 3 Disabled State -->
          <div v-if="(activeStep === 'preview' || activeStep === 'management') && !hasGeneratedData" class="px-6 py-12 text-center">
            <div class="text-gray-400">
              <svg class="mx-auto h-12 w-12 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m0 0v2m0-2h2m-2 0h-2m9-5a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <h3 class="text-lg font-medium text-gray-400 mb-2">Generate RDF First</h3>
              <p class="text-gray-400">Please complete Step 1 to generate your RDF graph before proceeding to GraphDB management.</p>
              <button
                @click="activeStep = 'generation'"
                class="mt-4 inline-flex items-center text-indigo-600 hover:text-indigo-800 font-medium"
              >
                Go to RDF Generation
                <svg class="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'GraphDBView',
  data() {
    return {
      activeStep: 'generation', // Track current active step
      formData: {
        baseUri: 'https://biodatafuse.org/example/',
        versionIri: 'https://biodatafuse.org/example/test.owl',
        authorName: '',
        authorEmail: '',
        orcid: '',
        graphName: 'my_graph',
        generateShacl: true,
        shaclThreshold: 0.001,
        generateUmlDiagram: true
      },
      generatedData: null,
      umlImageUrl: null,
      rdfContent: null,
      loading: false,
      loadingMessage: '',
      errorMessage: '',
      
      // GraphDB specific data
      graphdbConfig: {
        baseUrl: 'http://localhost:7200',
        repositoryName: '',
        username: '',
        password: ''
      },
      repositories: [],
      graphdbLoading: false,
      graphdbLoadingMessage: '',
      graphdbStatusMessage: '',
      graphdbErrorMessage: ''
    }
  },
  computed: {
    hasGeneratedData() {
      return this.generatedData && this.generatedData.generated_files && this.generatedData.generated_files.length > 0
    },
    umlFile() {
      return this.generatedData?.generated_files?.find(f => f.name.includes('uml') || f.name.endsWith('.png'))
    },
    rdfFile() {
      return this.generatedData?.generated_files?.find(f => f.type === 'RDF' || f.name.endsWith('.ttl') || f.name.endsWith('.rdf'))
    },
    isFormValid() {
      return this.formData.baseUri.trim() && 
             this.formData.versionIri.trim() &&
             this.formData.authorName.trim() && 
             this.formData.authorEmail.trim() && 
             this.formData.orcid.trim() && 
             this.formData.graphName.trim()
    }
  },
  mounted() {
    this.loadStoredData()
  },
  methods: {
    loadStoredData() {
      const storedData = localStorage.getItem('rdfGraphData')
      if (storedData) {
        try {
          this.generatedData = JSON.parse(storedData)
          if (this.umlFile) {
            this.fetchFilePreview(this.umlFile, 'image')
          }
          if (this.rdfFile) {
            this.fetchFilePreview(this.rdfFile, 'text')
          }
          // If we have generated data, allow navigation to step 2
          if (this.hasGeneratedData) {
            // Stay on generation step to show the results, but enable step 2 navigation
          }
        } catch (e) {
          console.error('Failed to parse stored RDF data:', e)
          localStorage.removeItem('rdfGraphData')
        }
      }
    },

    async generateRDF() {
      if (!this.isFormValid) return

      this.clearMessages()
      this.loading = true
      this.loadingMessage = 'Generating RDF graph...'

      try {
        const identifierSetId = localStorage.getItem('currentIdentifierSetId')
        if (!identifierSetId || isNaN(Number(identifierSetId))) {
          throw new Error('No valid identifier set found. Please complete the previous steps.')
        }

        const response = await axios.post('/api/rdf/generate', {
          identifier_set_id: Number(identifierSetId),
          base_uri: this.formData.baseUri,
          version_iri: this.formData.versionIri,
          author_name: this.formData.authorName,
          author_email: this.formData.authorEmail,
          orcid: this.formData.orcid,
          graph_name: this.formData.graphName,
          generate_shacl: this.formData.generateShacl,
          shacl_threshold: this.formData.shaclThreshold,
          generate_uml_diagram: this.formData.generateUmlDiagram
        })

        this.generatedData = response.data
        localStorage.setItem('rdfGraphData', JSON.stringify(this.generatedData))
        
        // Fetch UML image if present
        if (this.umlFile) {
          this.fetchFilePreview(this.umlFile, 'image')
        }
        if (this.rdfFile) {
          this.fetchFilePreview(this.rdfFile, 'text')
        }

        // Auto-advance to preview step after successful generation
        setTimeout(() => {
          this.activeStep = 'preview'
        }, 1500)

      } catch (error) {
        this.errorMessage = error.response?.data?.detail || error.message || 'Failed to generate RDF graph'
        console.error('RDF generation error:', error)
      } finally {
        this.loading = false
        this.loadingMessage = ''
      }
    },

    async fetchFilePreview(file, type) {
      try {
        if (type === 'image') {
          const response = await axios.get(`/api/rdf/download/${file.id}`, {
            responseType: 'blob'
          })
          this.umlImageUrl = URL.createObjectURL(response.data)
        } else if (type === 'text') {
          const response = await axios.get(`/api/rdf/download/${file.id}`, {
            responseType: 'text'
          })
          // Show first 2000 characters
          this.rdfContent = response.data.substring(0, 2000) + (response.data.length > 2000 ? '\n...' : '')
        }
      } catch (error) {
        console.error('Failed to fetch file preview:', error)
      }
    },

    async downloadFile(file) {
      try {
        const response = await axios.get(`/api/rdf/download/${file.id}`, {
          responseType: 'blob'
        })
        
        const url = URL.createObjectURL(response.data)
        const a = document.createElement('a')
        a.href = url
        a.download = file.name
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
      } catch (error) {
        this.errorMessage = 'Failed to download file'
      }
    },

    async downloadAllFiles() {
      for (const file of this.generatedData.generated_files) {
        await this.downloadFile(file)
        // Small delay between downloads
        await new Promise(resolve => setTimeout(resolve, 100))
      }
    },

    regenerateRdf() {
      this.generatedData = null
      this.umlImageUrl = null
      this.rdfContent = null
      localStorage.removeItem('rdfGraphData')
      this.clearMessages()
      // Go back to generation step
      this.activeStep = 'generation'
    },

    clearMessages() {
      this.errorMessage = ''
    },

    clearGraphDBMessages() {
      this.graphdbStatusMessage = ''
      this.graphdbErrorMessage = ''
    },

    setGraphDBLoading(isLoading, message = '') {
      this.graphdbLoading = isLoading
      this.graphdbLoadingMessage = message
    },

    selectRepository(repositoryId) {
      this.graphdbConfig.repositoryName = repositoryId
      this.clearGraphDBMessages()
    },

    // GraphDB Methods
    async testGraphDBConnection() {
      this.clearGraphDBMessages()
      this.setGraphDBLoading(true, 'Testing connection...')
      
      try {
        const response = await axios.post('/api/graphdb/test-connection', {
          baseUrl: this.graphdbConfig.baseUrl,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        this.graphdbStatusMessage = response.data.message
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Connection failed'
      } finally {
        this.setGraphDBLoading(false)
      }
    },

    async listRepositories() {
      this.clearGraphDBMessages()
      this.setGraphDBLoading(true, 'Fetching repositories...')
      
      try {
        const response = await axios.post('/api/graphdb/list-repositories', {
          baseUrl: this.graphdbConfig.baseUrl,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        this.repositories = response.data.repositories || []
        this.graphdbStatusMessage = `Found ${this.repositories.length} repositories`
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to fetch repositories'
      } finally {
        this.setGraphDBLoading(false)
      }
    },

    async createRepository() {
      this.clearGraphDBMessages()
      this.setGraphDBLoading(true, 'Creating repository...')
      
      try {
        const response = await axios.post('/api/graphdb/create-repository', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryName: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        this.graphdbStatusMessage = response.data.message
        // Refresh repository list
        await this.listRepositories()
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to create repository'
      } finally {
        this.setGraphDBLoading(false)
      }
    },

    async uploadRDFGraph() {
      this.clearGraphDBMessages()
      this.setGraphDBLoading(true, 'Uploading RDF graph data...')
      
      try {
        const response = await axios.post('/api/graphdb/upload-rdf', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryId: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null,
          graphData: this.generatedData
        })
        this.graphdbStatusMessage = response.data.message
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to upload RDF graph data'
      } finally {
        this.setGraphDBLoading(false)
      }
    },

    async countTriples() {
      this.clearGraphDBMessages()
      this.setGraphDBLoading(true, 'Counting triples...')
      
      try {
        const response = await axios.post('/api/graphdb/count-triples', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryName: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        this.graphdbStatusMessage = response.data.message
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to count triples'
      } finally {
        this.setGraphDBLoading(false)
      }
    },

    async deleteRepository() {
      if (!confirm(`Are you sure you want to delete repository "${this.graphdbConfig.repositoryName}"? This action cannot be undone.`)) {
        return
      }

      this.clearGraphDBMessages()
      this.setGraphDBLoading(true, 'Deleting repository...')
      
      try {
        const response = await axios.post('/api/graphdb/delete-repository', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryName: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        this.graphdbStatusMessage = response.data.message
        this.graphdbConfig.repositoryName = ''
        // Refresh repository list
        await this.listRepositories()
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to delete repository'
      } finally {
        this.setGraphDBLoading(false)
      }
    },

    onImageError() {
      console.error('Failed to load UML image')
      this.umlImageUrl = null
    },

    formatFileSize(bytes) {
      if (!bytes) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },

    formatDate(dateString) {
      if (!dateString) return ''
      return new Date(dateString).toLocaleString()
    }
  }
}
</script>