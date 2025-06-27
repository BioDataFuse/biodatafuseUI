<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Header Section -->
      <div class="text-center mb-12">
        <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
          GraphDB Integration
        </h1>
        <p class="mt-4 text-xl text-gray-600 max-w-3xl mx-auto">
          Generate RDF graphs from your biological data and  upload them to GraphDB
        </p>
      </div>

      <!-- Progress Indicator -->
      <div class="mb-8">
        <div class="flex items-center justify-center space-x-4">
          <div v-for="(step, index) in steps" :key="step.name" class="flex items-center">
            <div 
              :class="[
                'flex items-center justify-center w-10 h-10 rounded-full text-sm font-medium',
                getStepStatus(index) === 'complete' ? 'bg-indigo-600 text-white' :
                getStepStatus(index) === 'current' ? 'bg-indigo-100 text-indigo-600 border-2 border-indigo-600' :
                'bg-gray-200 text-gray-500'
              ]"
            >
              <svg v-if="getStepStatus(index) === 'complete'" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd" />
              </svg>
              <span v-else>{{ index + 1 }}</span>
            </div>
            <div v-if="index < steps.length - 1" :class="[
              'w-16 h-0.5 mx-3',
              getStepStatus(index) === 'complete' ? 'bg-indigo-600' : 'bg-gray-200'
            ]"></div>
          </div>
        </div>
        <div class="flex justify-center mt-3">
          <span class="text-sm text-gray-600">{{ steps[currentStepIndex].description }}</span>
        </div>
      </div>

      <!-- Main Content Card -->
      <div class="bg-white rounded-2xl shadow-xl overflow-hidden">
        <!-- Step 1: RDF Generation -->
        <div v-if="currentStepIndex === 0" class="p-8">
          <div class="flex items-center mb-6">
            <div class="bg-indigo-100 p-3 rounded-lg mr-4">
              <svg class="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-gray-900">Generate RDF Graph</h2>
              <p class="text-gray-600">Configure and create your RDF graph from biological annotation data</p>
            </div>
          </div>

          <!-- Compact Form -->
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <!-- Left Column -->
            <div class="space-y-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Graph Information</label>
                <div class="space-y-4">
                  <input
                    type="text"
                    v-model="formData.graphName"
                    placeholder="Graph name (e.g., my_gene_analysis)"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <input
                    type="url"
                    v-model="formData.baseUri"
                    placeholder="Base URI (e.g., https://biodatafuse.org/example/)"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <input
                    type="url"
                    v-model="formData.versionIri"
                    placeholder="Version IRI (e.g., https://biodatafuse.org/example/test.owl)"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Author Information</label>
                <div class="space-y-4">
                  <input
                    type="text"
                    v-model="formData.authorName"
                    placeholder="Your name"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <input
                    type="email"
                    v-model="formData.authorEmail"
                    placeholder="your.email@example.com"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                  <input
                    type="url"
                    v-model="formData.orcid"
                    placeholder="ORCID (e.g., https://orcid.org/0000-0000-0000-0000)"
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  />
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Schema Generation</label>
                <div class="space-y-3">
                  <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                    <input type="checkbox" v-model="formData.generateShacl" class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                    <div class="ml-3 flex-1">
                      <div class="text-sm font-medium text-gray-900">SHACL Shapes</div>
                      <div class="text-sm text-gray-500">Generate validation schemas</div>
                    </div>
                    <div v-if="formData.generateShacl" class="ml-2">
                      <input
                        type="number"
                        v-model.number="formData.shaclThreshold"
                        step="0.001"
                        min="0"
                        max="1"
                        placeholder="0.001"
                        class="w-20 px-2 py-1 text-xs border border-gray-300 rounded focus:ring-1 focus:ring-indigo-500"
                      />
                    </div>
                  </label>
                  <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                    <input type="checkbox" v-model="formData.generateShex" class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                    <div class="ml-3 flex-1">
                      <div class="text-sm font-medium text-gray-900">ShEx Shapes</div>
                      <div class="text-sm text-gray-500">Generate shape expressions</div>
                    </div>
                    <div v-if="formData.generateShex" class="ml-2">
                      <input
                        type="number"
                        v-model.number="formData.shexThreshold"
                        step="0.001"
                        min="0"
                        max="1"
                        placeholder="0.001"
                        class="w-20 px-2 py-1 text-xs border border-gray-300 rounded focus:ring-1 focus:ring-indigo-500"
                      />
                    </div>
                  </label>
                  <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                    <input type="checkbox" v-model="formData.generateUmlDiagram" class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                    <div class="ml-3">
                      <div class="text-sm font-medium text-gray-900">UML Diagrams</div>
                      <div class="text-sm text-gray-500">Visual representation</div>
                    </div>
                  </label>
                </div>
              </div>

              <!-- Namespace Section -->
              <div>
                <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                  <input type="checkbox" v-model="formData.enableCustomNamespaces" class="rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                  <div class="ml-3">
                    <div class="text-sm font-medium text-gray-900">Custom Namespaces</div>
                    <div class="text-sm text-gray-500">Add prefix shortcuts for querying</div>
                  </div>
                </label>
                
                <div v-if="formData.enableCustomNamespaces" class="mt-4 space-y-3">
                  <div v-for="(namespace, index) in formData.customNamespaces" :key="index" class="flex gap-2">
                    <input
                      v-model="namespace.prefix"
                      placeholder="foaf"
                      class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <input
                      v-model="namespace.uri"
                      placeholder="http://xmlns.com/foaf/0.1/"
                      class="flex-2 px-3 py-2 text-sm border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <button @click="removeNamespace(index)" class="text-red-500 hover:text-red-700 p-2">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                      </svg>
                    </button>
                  </div>
                  <button @click="addNamespace" class="text-sm text-indigo-600 hover:text-indigo-800 font-medium">
                    + Add namespace
                  </button>
                  
                  <!-- Quick add common namespaces -->
                  <div class="mt-3 pt-3 border-t border-gray-200">
                    <p class="text-xs text-gray-500 mb-2">Quick add:</p>
                    <div class="flex flex-wrap gap-2">
                      <button
                        v-for="common in commonNamespaces"
                        :key="common.prefix"
                        @click="addCommonNamespace(common)"
                        class="text-xs bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded transition-colors"
                      >
                        {{ common.prefix }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Status Messages -->
          <div v-if="loading || errorMessage" class="mb-6">
            <div v-if="loading" class="flex items-center p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500 mr-3"></div>
              <span class="text-blue-700">{{ loadingMessage }}</span>
            </div>
            <div v-if="errorMessage" class="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-red-700">{{ errorMessage }}</p>
            </div>
          </div>

          <!-- Action Button -->
          <div class="mt-8 flex justify-between px-6 py-4 bg-white rounded-b-xl shadow-lg">
            <button
              @click="goBack"
              class="px-4 py-2 border border-indigo-600 text-indigo-600 font-semibold rounded-lg hover:bg-indigo-100"
            >
              ← Select another visualization tool
            </button>
            <button
              @click="generateRDF"
              :disabled="loading || !isFormValid"
              class="px-8 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all duration-200"
            >
              <span v-if="loading" class="flex items-center">
                <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Generating...
              </span>
              <span v-else>Generate RDF Graph</span>
            </button>
          </div>
        </div>

        <!-- Step 2: Preview & Configure -->
        <div v-else-if="currentStepIndex === 1" class="p-8">
          <div class="flex items-center mb-6">
            <div class="bg-green-100 p-3 rounded-lg mr-4">
              <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-gray-900">Graph Generated Successfully</h2>
              <p class="text-gray-600">{{ generatedData?.generated_files?.length || 0 }} files created • Ready to upload to GraphDB</p>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-5 gap-8">
            <!-- Files Preview -->
            <div class="lg:col-span-2">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Generated Files</h3>
              <div class="bg-gray-50 rounded-lg max-h-64 overflow-y-auto">
                <div v-if="!generatedData?.generated_files?.length" class="p-6 text-center text-gray-500">
                  <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <p class="text-sm">No files generated yet</p>
                </div>
                
                <div v-else class="divide-y divide-gray-200">
                  <div v-for="file in generatedData?.generated_files" :key="file.id" 
                       class="flex items-center justify-between p-4 hover:bg-white transition-colors">
                    <div class="flex items-center min-w-0 flex-1">
                      <div class="w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center mr-3 flex-shrink-0">
                        <svg class="w-5 h-5 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                      </div>
                      <div class="min-w-0 flex-1">
                        <div class="font-medium text-gray-900 truncate">{{ file.name }}</div>
                        <div class="text-sm text-gray-500">{{ file.type }} • {{ formatFileSize(file.size) }}</div>
                      </div>
                    </div>
                    <button @click="downloadFile(file)" class="text-indigo-600 hover:text-indigo-800 font-medium text-sm ml-3 flex-shrink-0">
                      Download
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Schema Visualization -->
            <div class="lg:col-span-3">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Schema Visualization</h3>
              <div class="space-y-4">
                <!-- Display selected UML diagram -->
                <div v-if="selectedVisualization && selectedUmlFile" class="bg-gray-50 rounded-lg p-4">
                  <div class="flex items-center justify-between mb-3">
                    <h4 class="text-sm font-medium text-gray-900">
                      {{ selectedVisualization === 'shacl' ? 'SHACL Schema' : 'ShEx Schema' }} UML Diagram
                    </h4>
                    <button 
                      @click="downloadFile(selectedUmlFile)" 
                      class="text-indigo-600 hover:text-indigo-800 text-sm font-medium flex items-center gap-1"
                    >
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                      </svg>
                      Download
                    </button>
                  </div>
                  <div class="bg-white rounded border overflow-hidden shadow-sm">
                    <div v-if="loadingImage" class="flex items-center justify-center p-8">
                      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500"></div>
                      <span class="ml-3 text-gray-600">Loading diagram...</span>
                    </div>
                    <img 
                      v-else-if="imageUrl"
                      :src="imageUrl" 
                      :alt="`${selectedVisualization} UML Diagram`"
                      class="w-full h-auto object-contain"
                      style="max-height: 600px;"
                      @error="handleImageError"
                    />
                    <div v-else class="flex items-center justify-center p-8 text-gray-500">
                      <span>Failed to load diagram</span>
                    </div>
                  </div>
                </div>
                
                <!-- No UML available message -->
                <div v-else-if="selectedVisualization && !selectedUmlFile" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <div class="flex">
                    <svg class="w-5 h-5 text-yellow-400 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                    </svg>
                    <div>
                      <h4 class="text-sm font-medium text-yellow-800">UML Diagram Not Available</h4>
                      <p class="text-sm text-yellow-700 mt-1">
                        UML diagram generation was not enabled for {{ selectedVisualization === 'shacl' ? 'SHACL' : 'ShEx' }} shapes during RDF generation.
                      </p>
                    </div>
                  </div>
                </div>
                
                <!-- Default message when no selection -->
                <div v-else class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div class="flex">
                    <svg class="w-5 h-5 text-blue-400 mr-3 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                    </svg>
                    <div>
                      <h4 class="text-sm font-medium text-blue-800">Schema Visualization</h4>
                      <p class="text-sm text-blue-700 mt-1">
                        Select a schema type above to view its UML diagram visualization.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
            <button @click="currentStepIndex = 0" class="text-gray-500 hover:text-gray-700 font-medium">
              ← Back to Generation
            </button>
              <button
                @click="currentStepIndex = 2"
                :disabled="!hasGeneratedData"
                class="px-8 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
              >
                Continue to Setup
              </button>
          </div>
        </div>

        <!-- Step 3: GraphDB Setup -->
        <div v-else-if="currentStepIndex === 2" class="p-8">
          <div class="flex items-center mb-6">
            <div class="bg-blue-100 p-3 rounded-lg mr-4">
              <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-gray-900">Setup GraphDB Repository</h2>
              <p class="text-gray-600">Configure connection and select or create a repository for your data</p>
            </div>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Repository Configuration -->
            <div>
              <div class="mb-8">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Repository Configuration</h3>
                <div class="bg-gray-50 rounded-lg p-6 space-y-4">
                  <!-- Connection Details -->
                  <div class="grid grid-cols-1 gap-4">
                    <input
                      type="url"
                      v-model="graphdbConfig.baseUrl"
                      placeholder="GraphDB URL (e.g., http://localhost:7200)"
                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    />
                    <div class="grid grid-cols-2 gap-4">
                      <input
                        type="text"
                        v-model="graphdbConfig.username"
                        placeholder="Username (optional)"
                        class="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      />
                      <input
                        type="password"
                        v-model="graphdbConfig.password"
                        placeholder="Password (optional)"
                        class="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      />
                    </div>
                  </div>

                  <!-- Create New Repository -->
                  <div v-if="connectionStatus?.type === 'success'" class="pt-4 border-t border-gray-200">
                    <div class="flex gap-3">
                      <input
                        type="text"
                        v-model="newRepositoryName"
                        placeholder="Repository name (e.g., my_biodata_graph)"
                        class="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      />
                      <button
                        @click="createRepository"
                        :disabled="graphdbLoading || !newRepositoryName.trim()"
                        class="px-4 py-2 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
                      >
                        <span v-if="graphdbLoading" class="flex items-center">
                          <div class="animate-spin rounded-full h-3 w-3 border-b-2 border-white mr-1"></div>
                          Creating...
                        </span>
                        <span v-else>Create</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Repository Sidebar -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <h3 class="text-lg font-semibold text-gray-900">Available Repositories</h3>
                <button 
                  @click="listRepositories" 
                  :disabled="!graphdbConfig.baseUrl || graphdbLoading"
                  class="text-sm text-indigo-600 hover:text-indigo-800 font-medium disabled:opacity-50"
                >
                  Refresh
                </button>
              </div>
              
              <div class="bg-gray-50 rounded-lg max-h-96 overflow-y-auto">
                <div v-if="!connectionStatus || connectionStatus.type !== 'success'" class="p-6 text-center text-gray-500">
                  <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <p class="text-sm">Test connection first</p>
                  <p class="text-xs text-gray-400 mt-1">Connect to GraphDB to see available repositories</p>
                </div>
                
                <div v-else-if="repositories.length === 0" class="p-6 text-center text-gray-500">
                  <svg class="mx-auto h-12 w-12 text-gray-400 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2M4 13h2m13-8l-8 8-4-4"></path>
                  </svg>
                  <p class="text-sm">No repositories found</p>
                  <p class="text-xs text-gray-400 mt-1">Create a new repository to get started</p>
                </div>
                
                <div v-else class="divide-y divide-gray-200">
                  <div v-for="repo in repositories" :key="repo.id" 
                       :class="[
                         'p-4 transition-colors',
                         graphdbConfig.repositoryName === repo.id ? 'bg-indigo-50 border-l-4 border-indigo-500' : 'hover:bg-white'
                       ]">
                    <div class="flex items-center justify-between mb-3">
                      <div 
                        class="min-w-0 flex-1 cursor-pointer"
                        @click="selectRepository(repo.id)"
                      >
                        <div class="font-medium text-gray-900 truncate">{{ repo.id }}</div>
                        <div class="text-sm text-gray-500 truncate">{{ repo.title || 'No description' }}</div>
                      </div>
                      <div v-if="graphdbConfig.repositoryName === repo.id" class="text-indigo-500 ml-2">
                        <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                        </svg>
                      </div>
                    </div>
                    
                    <!-- Repository Status -->
                    <div class="flex space-x-2 mb-3">
                      <span :class="[
                        'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                        repo.readable ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
                      ]">
                        {{ repo.readable ? 'Readable' : 'Not Readable' }}
                      </span>
                      <span :class="[
                        'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                        repo.writable ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700'
                      ]">
                        {{ repo.writable ? 'Writable' : 'Read Only' }}
                      </span>
                    </div>

                    <!-- Repository Actions -->
                    <div class="flex space-x-2">
                      <button
                        @click="confirmDeleteRepository(repo.id)"
                        :disabled="graphdbLoading"
                        class="px-3 py-1 text-xs border border-red-300 text-red-700 font-medium rounded hover:bg-red-50 disabled:opacity-50"
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
            <button @click="currentStepIndex = 1" class="text-gray-500 hover:text-gray-700 font-medium">
              ← Back to Preview
            </button>
            <button
              @click="currentStepIndex = 3"
              :disabled="!graphdbConfig.repositoryName"
              class="px-8 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
            >
              Continue to Upload
            </button>
          </div>
        </div>

        <!-- Step 4: Upload Data -->
        <div v-else-if="currentStepIndex === 3" class="p-8">
          <div class="flex items-center mb-6">
            <div class="bg-purple-100 p-3 rounded-lg mr-4">
              <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
            </div>
            <div>
              <h2 class="text-2xl font-bold text-gray-900">Upload Data to GraphDB</h2>
              <p class="text-gray-600">Upload your RDF graph and schemas to repository: <strong>{{ graphdbConfig.repositoryName }}</strong></p>
            </div>
          </div>



          <!-- Upload Options -->
          <div class="mb-8">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Select items to upload</h3>
            <div class="space-y-4">
              <!-- RDF Graph -->
              <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div class="flex items-center">
                  <input 
                    type="checkbox" 
                    id="upload-rdf"
                    v-model="uploadSelections.rdf" 
                    :disabled="!hasGeneratedData || isUploading('rdf')"
                    class="rounded border-gray-300 text-gray-900 focus:ring-gray-500"
                  />
                  <label for="upload-rdf" class="ml-3">
                    <div class="font-medium text-gray-900">RDF Graph</div>
                    <div class="text-sm text-gray-500">Core RDF triples containing your biological data and annotations</div>
                  </label>
                </div>
                <div class="flex items-center space-x-2">
                  <span v-if="uploadStatus.rdf === 'success'" class="text-green-600 text-sm">✓ Uploaded</span>
                  <span v-else-if="isUploading('rdf')" class="text-gray-500 text-sm flex items-center">
                    <div class="animate-spin rounded-full h-3 w-3 border-b-2 border-gray-500 mr-1"></div>
                    Uploading...
                  </span>
                </div>
              </div>

              <!-- SHACL Shapes -->
              <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg" :class="{ 'opacity-50': !formData.generateShacl }">
                <div class="flex items-center">
                  <input 
                    type="checkbox" 
                    id="upload-shacl"
                    v-model="uploadSelections.shacl" 
                    :disabled="!formData.generateShacl || isUploading('shacl')"
                    class="rounded border-gray-300 text-gray-900 focus:ring-gray-500"
                  />
                  <label for="upload-shacl" class="ml-3">
                    <div class="font-medium text-gray-900">SHACL Shapes</div>
                    <div class="text-sm text-gray-500">
                      {{ formData.generateShacl ? 'Data validation schemas' : 'Not generated - SHACL was disabled' }}
                    </div>
                  </label>
                </div>
                <div class="flex items-center space-x-2">
                  <span v-if="uploadStatus.shacl === 'success'" class="text-green-600 text-sm">✓ Uploaded</span>
                  <span v-else-if="isUploading('shacl')" class="text-gray-500 text-sm flex items-center">
                    <div class="animate-spin rounded-full h-3 w-3 border-b-2 border-gray-500 mr-1"></div>
                    Uploading...
                  </span>
                </div>
              </div>

              <!-- ShEx Shapes -->
              <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg" :class="{ 'opacity-50': !formData.generateShex }">
                <div class="flex items-center">
                  <input 
                    type="checkbox" 
                    id="upload-shex"
                    v-model="uploadSelections.shex" 
                    :disabled="!formData.generateShex || isUploading('shex')"
                    class="rounded border-gray-300 text-gray-900 focus:ring-gray-500"
                  />
                  <label for="upload-shex" class="ml-3">
                    <div class="font-medium text-gray-900">ShEx Shapes</div>
                    <div class="text-sm text-gray-500">
                      {{ formData.generateShex ? 'Shape expressions for RDF validation' : 'Not generated - ShEx was disabled' }}
                    </div>
                  </label>
                </div>
                <div class="flex items-center space-x-2">
                  <span v-if="uploadStatus.shex === 'success'" class="text-green-600 text-sm">✓ Uploaded</span>
                  <span v-else-if="isUploading('shex')" class="text-gray-500 text-sm flex items-center">
                    <div class="animate-spin rounded-full h-3 w-3 border-b-2 border-gray-500 mr-1"></div>
                    Uploading...
                  </span>
                </div>
              </div>

              <!-- Custom Namespaces -->
              <div class="flex items-center justify-between p-4 border border-gray-200 rounded-lg" :class="{ 'opacity-50': !formData.enableCustomNamespaces }">
                <div class="flex items-center">
                  <input 
                    type="checkbox" 
                    id="upload-namespaces"
                    v-model="uploadSelections.namespaces" 
                    :disabled="!formData.enableCustomNamespaces || isUploading('namespaces')"
                    class="rounded border-gray-300 text-gray-900 focus:ring-gray-500"
                  />
                  <label for="upload-namespaces" class="ml-3">
                    <div class="font-medium text-gray-900">Custom Namespaces</div>
                    <div class="text-sm text-gray-500">
                      {{ formData.enableCustomNamespaces ? 'Custom namespace prefixes for SPARQL queries' : 'No custom namespaces configured' }}
                    </div>
                  </label>
                </div>
                <div class="flex items-center space-x-2">
                  <span v-if="uploadStatus.namespaces === 'success'" class="text-green-600 text-sm">✓ Uploaded</span>
                  <span v-else-if="isUploading('namespaces')" class="text-gray-500 text-sm flex items-center">
                    <div class="animate-spin rounded-full h-3 w-3 border-b-2 border-gray-500 mr-1"></div>
                    Uploading...
                  </span>
                </div>
              </div>
            </div>

            <!-- Upload Actions -->
            <div class="flex items-center justify-between mt-6 pt-4 border-t border-gray-200">
              <div class="flex items-center space-x-4">
                <button
                  @click="selectAll"
                  class="text-sm text-gray-600 hover:text-gray-800 font-medium"
                >
                  Select All Available
                </button>
                <button
                  @click="selectNone"
                  class="text-sm text-gray-600 hover:text-gray-800 font-medium"
                >
                  Select None
                </button>
              </div>
              <button
                @click="uploadSelected"
                :disabled="!hasSelectedItems || isAnyUploading"
                class="px-6 py-2 bg-gray-900 text-white font-medium rounded-lg hover:bg-gray-800 disabled:opacity-50 disabled:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors"
              >
                <span v-if="isAnyUploading">Uploading...</span>
                <span v-else>Upload Selected</span>
              </button>
            </div>
          </div>

          <!-- Status Messages -->
          <div v-if="graphdbStatusMessage || graphdbErrorMessage" class="mb-6">
            <div v-if="graphdbStatusMessage" class="p-3 bg-green-50 border border-green-200 rounded-lg text-green-700">
              <div class="flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
                {{ graphdbStatusMessage }}
              </div>
            </div>
            <div v-if="graphdbErrorMessage" class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700">
              <div class="flex items-center">
                <svg class="w-5 h-5 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {{ graphdbErrorMessage }}
              </div>
            </div>
          </div>

          <!-- Upload Summary -->
          <div class="bg-gray-50 rounded-lg p-6 mb-6">
            <h3 class="text-lg font-semibold text-gray-900 mb-4">Upload Summary</h3>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="text-center">
                <div class="text-2xl font-bold" :class="uploadStatus.rdf === 'success' ? 'text-green-600' : 'text-gray-400'">
                  {{ uploadStatus.rdf === 'success' ? '✓' : '○' }}
                </div>
                <div class="text-sm text-gray-600">RDF Graph</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold" :class="uploadStatus.shacl === 'success' ? 'text-green-600' : 'text-gray-400'">
                  {{ uploadStatus.shacl === 'success' ? '✓' : '○' }}
                </div>
                <div class="text-sm text-gray-600">SHACL Shapes</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold" :class="uploadStatus.shex === 'success' ? 'text-green-600' : 'text-gray-400'">
                  {{ uploadStatus.shex === 'success' ? '✓' : '○' }}
                </div>
                <div class="text-sm text-gray-600">ShEx Shapes</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold" :class="uploadStatus.namespaces === 'success' ? 'text-green-600' : 'text-gray-400'">
                  {{ uploadStatus.namespaces === 'success' ? '✓' : '○' }}
                </div>
                <div class="text-sm text-gray-600">Namespaces</div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-between items-center mt-8 pt-6 border-t border-gray-200">
            <button @click="currentStepIndex = 2" class="text-gray-500 hover:text-gray-700 font-medium">
              ← Back to Setup
            </button>
            <div class="flex space-x-3">
              <button
                @click="resetWorkflow"
                class="px-6 py-3 border border-gray-300 text-gray-700 font-medium rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
              >
                Start Over
              </button>
              <button
                v-if="uploadStatus.rdf === 'success'"
                @click="openGraphDBWorkbench"
                class="px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
              >
                Open GraphDB Workbench
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete Confirmation Modal -->
  <div v-if="showDeleteConfirm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
      <h3 class="text-lg font-semibold text-gray-900 mb-4">Confirm Repository Deletion</h3>
      <p class="text-sm text-gray-600 mb-6">
        Are you sure you want to delete the repository <strong>{{ repositoryToDelete }}</strong>? 
        This action cannot be undone and will permanently remove all data in this repository.
      </p>
      <div class="flex justify-end space-x-3">
        <button
          @click="showDeleteConfirm = false; repositoryToDelete = ''"
          class="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          Cancel
        </button>
        <button
          @click="deleteRepository"
          :disabled="graphdbLoading"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50"
        >
          <span v-if="graphdbLoading">Deleting...</span>
          <span v-else>Delete Repository</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

// Upload Card Component
const UploadCard = {
  props: ['title', 'description', 'disabled', 'loading'],
  emits: ['click'],
  template: `
    <button
      @click="$emit('click')"
      :disabled="disabled"
      class="p-4 border-2 border-dashed border-gray-300 rounded-lg hover:border-indigo-400 hover:bg-indigo-50 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
      :class="{ 'border-indigo-400 bg-indigo-50': loading }"
    >
      <div class="flex items-center justify-between mb-2">
        <h4 class="font-medium text-gray-900">{{ title }}</h4>
        <div v-if="loading" class="animate-spin rounded-full h-4 w-4 border-b-2 border-indigo-500"></div>
      </div>
      <p class="text-sm text-gray-500">{{ description }}</p>
    </button>
  `
}

export default {
  name: 'GraphDBView',
  components: {
    UploadCard
  },
  data() {
    return {
      currentStepIndex: 0,
      steps: [
        { name: 'Graph Generation', description: 'Create RDF graph from your biological data' },
        { name: 'Preview & Configure', description: 'Preview generated files and configure settings' },
        { name: 'GraphDB Setup', description: 'Configure GraphDB connection and repository' },
        { name: 'Upload Data', description: 'Upload your data and schemas to GraphDB' }
      ],
      formData: {
        baseUri: 'https://biodatafuse.org/example/',
        versionIri: 'https://biodatafuse.org/example/test.owl',
        authorName: '',
        authorEmail: '',
        orcid: 'https://orcid.org/0000-0000-0000-0000',
        graphName: 'my_graph',
        generateShacl: true,
        shaclThreshold: 0.001,
        generateUmlDiagram: true,
        generateShex: true,
        shexThreshold: 0.001,
        enableCustomNamespaces: false,
        customNamespaces: []
      },
      commonNamespaces: [
        { prefix: 'foaf', uri: 'http://xmlns.com/foaf/0.1/' },
        { prefix: 'dc', uri: 'http://purl.org/dc/elements/1.1/' },
        { prefix: 'dcterms', uri: 'http://purl.org/dc/terms/' },
        { prefix: 'skos', uri: 'http://www.w3.org/2004/02/skos/core#' },
        { prefix: 'owl', uri: 'http://www.w3.org/2002/07/owl#' },
        { prefix: 'rdfs', uri: 'http://www.w3.org/2000/01/rdf-schema#' },
        { prefix: 'xsd', uri: 'http://www.w3.org/2001/XMLSchema#' }
      ],
      generatedData: null,
      loading: false,
      loadingMessage: '',
      errorMessage: '',
      graphdbConfig: {
        baseUrl: 'http://localhost:7200',
        repositoryName: '',
        username: '',
        password: ''
      },
      repositories: [],
      connectionStatus: null,
      graphdbLoading: false,
      graphdbStatusMessage: '',
      graphdbErrorMessage: '',
      uploadingItems: new Set(),
      newRepositoryName: '',
      showDeleteConfirm: false,
      selectedVisualization: '',
      loadingImage: false,
      imageUrl: null,
      repositoryToDelete: '',
      autoTestTimeout: null,
      uploadStatus: {
        rdf: null,      // null, 'uploading', 'success', 'error'
        shacl: null,
        shex: null,
        namespaces: null
      },
      uploadSelections: {
        rdf: true,
        shacl: false,
        shex: false,
        namespaces: false
      },
    }
  },
  computed: {
    hasGeneratedData() {
      return this.generatedData && this.generatedData.generated_files && this.generatedData.generated_files.length > 0
    },
    isFormValid() {
      return this.formData.baseUri.trim() && 
             this.formData.versionIri.trim() &&
             this.formData.authorName.trim() && 
             this.formData.authorEmail.trim() && 
             this.formData.orcid.trim() &&
             this.formData.graphName.trim()
    },
    isConnectionValid() {
      return this.connectionStatus && this.connectionStatus.type === 'success'
    },
    selectedUmlFile() {
      if (!this.selectedVisualization || !this.generatedData?.generated_files) return null
      
      const fileName = this.selectedVisualization === 'shacl' 
        ? `${this.formData.graphName}_shacl.png`
        : `${this.formData.graphName}_shex_diagram.png`
      
      return this.generatedData.generated_files.find(file => file.name === fileName)
    },

    defaultVisualization() {
      if (!this.generatedData?.generated_files) return ''
      
      // Check if SHACL UML is available
      if (this.formData.generateShacl && this.formData.generateUmlDiagram) {
        const shaclFile = this.generatedData.generated_files.find(file => 
          file.name === `${this.formData.graphName}_shacl.png`
        )
        if (shaclFile) return 'shacl'
      }
      
      // Check if ShEx UML is available
      if (this.formData.generateShex && this.formData.generateUmlDiagram) {
        const shexFile = this.generatedData.generated_files.find(file => 
          file.name === `${this.formData.graphName}_shex_diagram.png`
        )
        if (shexFile) return 'shex'
      }
      
      return ''
    },
    hasSelectedItems() {
      return Object.values(this.uploadSelections).some(selected => selected)
    },
    isAnyUploading() {
      return this.uploadingItems.size > 0
    }
  },

  watch: {
    // Watch for step changes to automatically load repositories when reaching step 2
    currentStepIndex(newStep, oldStep) {
      if (newStep === 2 && oldStep === 1) {
        // When moving to step 3, auto-test connection if it's a localhost URL
        this.autoTestConnection()
      }
    },
    
    // Watch for changes to the GraphDB URL
    'graphdbConfig.baseUrl': {
      handler(newUrl) {
        if (this.currentStepIndex === 2 && newUrl) {
          // Auto-test connection when URL changes in step 3
          this.autoTestConnection()
        }
      },
      immediate: false
    },

    selectedUmlFile: {
      handler(newFile) {
        if (newFile) {
          this.loadImagePreview(newFile)
        } else {
          this.imageUrl = null
        }
      },
      immediate: true
    },
    defaultVisualization: {
      handler(newDefault) {
        if (newDefault && !this.selectedVisualization) {
          this.selectedVisualization = newDefault
        }
      },
      immediate: true
    }
  },
  mounted() {
    this.loadStoredData()
    
    // If we're already on step 2 and have a GraphDB URL, load repositories
    if (this.currentStepIndex === 1 && this.graphdbConfig.baseUrl) {
      this.listRepositories()
    }
  },
  methods: {
    getStepStatus(index) {
      if (index < this.currentStepIndex) return 'complete'
      if (index === this.currentStepIndex) return 'current'
      return 'upcoming'
    },

    async generateRDF() {
      if (!this.isFormValid) {
        this.errorMessage = 'Please fill in all required fields before generating the RDF graph.'
        return
      }

      this.loading = true
      this.loadingMessage = 'Generating RDF graph...'
      this.errorMessage = ''

      try {
        const identifierSetId = localStorage.getItem('currentIdentifierSetId')
        if (!identifierSetId || isNaN(Number(identifierSetId))) {
          throw new Error('No valid identifier set found. Please complete the previous steps in the query builder.')
        }

        console.log('Generating RDF with data:', {
          identifier_set_id: Number(identifierSetId),
          base_uri: this.formData.baseUri,
          version_iri: this.formData.versionIri,
          author_name: this.formData.authorName,
          author_email: this.formData.authorEmail,
          orcid: this.formData.orcid,
          graph_name: this.formData.graphName,
          generate_shacl: this.formData.generateShacl,
          shacl_threshold: this.formData.shaclThreshold,
          generate_uml_diagram: this.formData.generateUmlDiagram,
          generate_shex: this.formData.generateShex,
          shex_threshold: this.formData.shexThreshold
        })

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
          generate_uml_diagram: this.formData.generateUmlDiagram,
          generate_shex: this.formData.generateShex,
          shex_threshold: this.formData.shexThreshold
        })

        console.log('RDF generation response:', response.data)
        this.generatedData = response.data
        localStorage.setItem('rdfGraphData', JSON.stringify(this.generatedData))
        
        // Auto-advance to next step
        setTimeout(() => {
          this.currentStepIndex = 1
        }, 1000)

      } catch (error) {
        console.error('RDF generation error:', error)
        
        // Enhanced error handling
        if (error.response) {
          // Server responded with error status
          const detail = error.response.data?.detail || error.response.data?.message || 'Unknown server error'
          this.errorMessage = `Server Error (${error.response.status}): ${detail}`
          
          // Specific error messages for common issues
          if (error.response.status === 400) {
            this.errorMessage = `Bad Request: ${detail}. Please check your input data and try again.`
          } else if (error.response.status === 404) {
            this.errorMessage = 'RDF generation service not found. Please contact the administrator.'
          } else if (error.response.status === 500) {
            this.errorMessage = `Internal Server Error: ${detail}. This appears to be a backend issue - please contact the administrator.`
          }
        } else if (error.request) {
          // Network error
          this.errorMessage = 'Network error: Could not connect to the server. Please check your internet connection and try again.'
        } else {
          // Client-side error
          this.errorMessage = error.message || 'Failed to generate RDF graph. Please try again.'
        }
      } finally {
        this.loading = false
        this.loadingMessage = ''
      }
    },

    async autoTestConnection() {
      // Only auto-test if it's a localhost URL and we haven't already tested
      if (this.graphdbConfig.baseUrl && 
          (this.graphdbConfig.baseUrl.includes('localhost') || this.graphdbConfig.baseUrl.includes('127.0.0.1')) &&
          (!this.connectionStatus || this.connectionStatus.type !== 'success')) {
        
        console.log('🔄 Auto-testing localhost connection...')
        
        // Add a small delay to avoid too frequent requests
        if (this.autoTestTimeout) {
          clearTimeout(this.autoTestTimeout)
        }
        
        this.autoTestTimeout = setTimeout(async () => {
          try {
            await this.testConnection()
          } catch (error) {
            console.log('Auto connection test failed, user can manually retry')
          }
        }, 500)
      }
    },

    async testConnection() {
      this.connectionStatus = null
      this.graphdbLoading = true
      this.graphdbErrorMessage = ''
      this.graphdbStatusMessage = ''
      
      try {
        const response = await axios.post('/api/graphdb/test-connection', {
          baseUrl: this.graphdbConfig.baseUrl,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        
        this.connectionStatus = { type: 'success', message: response.data.message }
        
        // Automatically fetch repositories after successful connection
        await this.listRepositories()
        
      } catch (error) {
        const errorMessage = error.response?.data?.detail || 'Connection failed. Please check your settings.'
        this.connectionStatus = { type: 'error', message: errorMessage }
      } finally {
        this.graphdbLoading = false
      }
    },

    isUploading(type) {
      return this.uploadingItems.has(type)
    },

    async uploadRDFGraph() {
      this.uploadingItems.add('rdf')
      this.uploadStatus.rdf = 'uploading'
      this.graphdbErrorMessage = ''
      
      try {
        console.log('🚀 Starting RDF upload with data:', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryId: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          hasGeneratedData: !!this.generatedData,
          generatedFilesCount: this.generatedData?.generated_files?.length || 0
        })

        // Validate required data before sending
        if (!this.generatedData) {
          throw new Error('No generated data available for upload')
        }

        if (!this.graphdbConfig.baseUrl) {
          throw new Error('GraphDB URL is required')
        }

        if (!this.graphdbConfig.repositoryName) {
          throw new Error('Repository name is required')
        }

        const payload = {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryId: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null,
          graphData: this.generatedData
        }

        console.log('📤 Sending RDF upload request with payload structure:', {
          baseUrl: payload.baseUrl,
          repositoryId: payload.repositoryId,
          username: payload.username,
          hasGraphData: !!payload.graphData,
          graphDataKeys: payload.graphData ? Object.keys(payload.graphData) : [],
          generatedFilesCount: payload.graphData?.generated_files?.length || 0,
          generationId: payload.graphData?.generation_id || 'NOT_FOUND'
        })

        // Log the full generated data structure for debugging
        console.log('🔍 Full generated data structure:', JSON.stringify(this.generatedData, null, 2))

        const response = await axios.post('/api/graphdb/upload-rdf', payload)
        
        console.log('✅ RDF upload successful:', response.data)
        this.graphdbStatusMessage = response.data.message || 'RDF graph uploaded successfully'
        this.uploadStatus.rdf = 'success'
        
      } catch (error) {
        console.error('❌ RDF upload failed:', error)
        
        let errorMessage = 'Failed to upload RDF graph'
        
        if (error.response) {
          // Server responded with error status
          const detail = error.response.data?.detail || error.response.data?.message
          errorMessage = `Upload failed (${error.response.status}): ${detail || 'Unknown server error'}`
          
          console.error('Full server error response:', {
            status: error.response.status,
            statusText: error.response.statusText,
            data: error.response.data,
            headers: error.response.headers
          })
          
          // Log the exact error detail for debugging
          if (error.response.data) {
            console.error('Server error detail:', JSON.stringify(error.response.data, null, 2))
          }
          
        } else if (error.request) {
          // Network error
          errorMessage = 'Network error: Could not connect to upload service'
        } else {
          // Client-side error
          errorMessage = error.message || errorMessage
        }
        
        this.graphdbErrorMessage = errorMessage
        this.uploadStatus.rdf = 'error'
        
      } finally {
        this.uploadingItems.delete('rdf')
      }
    },

    async uploadShaclPrefixes() {
      this.uploadingItems.add('shacl')
      this.uploadStatus.shacl = 'uploading'
      this.graphdbErrorMessage = ''
      
      try {
        const response = await axios.post('/api/graphdb/upload-prefixes', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryId: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null,
          graphData: this.generatedData
        })
        this.graphdbStatusMessage = response.data.message
        this.uploadStatus.shacl = 'success'
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to upload SHACL shapes'
        this.uploadStatus.shacl = 'error'
      } finally {
        this.uploadingItems.delete('shacl')
      }
    },

    async uploadShexShapes() {
      this.uploadingItems.add('shex')
      this.uploadStatus.shex = 'uploading'
      this.graphdbErrorMessage = ''
      
      try {
        const response = await axios.post('/api/graphdb/upload-shex', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryId: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null,
          graphData: this.generatedData
        })
        this.graphdbStatusMessage = response.data.message
        this.uploadStatus.shex = 'success'
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to upload ShEx shapes'
        this.uploadStatus.shex = 'error'
      } finally {
        this.uploadingItems.delete('shex')
      }
    },

    async uploadCustomNamespaces() {
      this.uploadingItems.add('namespaces')
      this.uploadStatus.namespaces = 'uploading'
      this.graphdbErrorMessage = ''
      
      try {
        const response = await axios.post('/api/graphdb/upload-namespaces', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryId: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null,
          graphData: {
            namespaces: Object.fromEntries(
              this.formData.customNamespaces.map(ns => [ns.prefix, ns.uri])
            )
          }
        })
        this.graphdbStatusMessage = response.data.message
        this.uploadStatus.namespaces = 'success'
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to upload namespaces'
        this.uploadStatus.namespaces = 'error'
      } finally {
        this.uploadingItems.delete('namespaces')
      }
    },

    openGraphDBWorkbench() {
      const workbenchUrl = `${this.graphdbConfig.baseUrl}/`
      window.open(workbenchUrl, '_blank')
    },

    resetWorkflow() {
      this.currentStepIndex = 0
      this.generatedData = null
      this.connectionStatus = null
      this.graphdbStatusMessage = ''
      this.graphdbErrorMessage = ''
      this.uploadingItems.clear()
      this.uploadStatus = {
        rdf: null,
        shacl: null,
        shex: null,
        namespaces: null
      }
      localStorage.removeItem('rdfGraphData')
    },

    loadStoredData() {
      const storedData = localStorage.getItem('rdfGraphData')
      if (storedData) {
        try {
          this.generatedData = JSON.parse(storedData)
          // Remove auto-advance - always start at step 1
          // if (this.hasGeneratedData) {
          //   this.currentStepIndex = 1
          // }
        } catch (e) {
          localStorage.removeItem('rdfGraphData')
        }
      }
    },

    addNamespace() {
      this.formData.customNamespaces.push({ prefix: '', uri: '' })
    },

    removeNamespace(index) {
      this.formData.customNamespaces.splice(index, 1)
    },

    selectRepository(repositoryId) {
      this.graphdbConfig.repositoryName = repositoryId
    },

    formatFileSize(bytes) {
      if (!bytes) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
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

    async listRepositories() {
      if (!this.graphdbConfig.baseUrl) {
        console.warn('No GraphDB URL provided for listing repositories')
        return
      }

      // Clear any previous error messages
      this.graphdbErrorMessage = ''
      this.graphdbStatusMessage = ''
      
      this.graphdbLoading = true
      try {
        console.log('🔍 Fetching repositories from:', this.graphdbConfig.baseUrl)
        
        const response = await axios.post('/api/graphdb/list-repositories', {
          baseUrl: this.graphdbConfig.baseUrl,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        
        console.log('📋 Repository response:', response.data)
        
        this.repositories = response.data.repositories || []
        
        if (this.repositories.length === 0) {
          this.graphdbStatusMessage = 'No repositories found in this GraphDB instance.'
        } else {
          this.graphdbStatusMessage = `Found ${this.repositories.length} repositories.`
          
        }
        
      } catch (error) {
        console.error('❌ Failed to fetch repositories:', error)
        const errorMessage = error.response?.data?.detail || 'Failed to fetch repositories'
        this.graphdbErrorMessage = errorMessage
        this.repositories = []
      } finally {

        this.graphdbLoading = false
      }
    },

    async createRepository() {
      if (!this.newRepositoryName.trim()) return
      
      this.graphdbLoading = true
      try {
        await axios.post('/api/graphdb/create-repository', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryName: this.newRepositoryName.trim(),
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        this.graphdbStatusMessage = `Repository '${this.newRepositoryName}' created successfully`
        this.newRepositoryName = '' // Clear the input
        await this.listRepositories()
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to create repository'
      } finally {
        this.graphdbLoading = false
      }
    },

    async countTriples(repositoryName = null) {
      const repoName = repositoryName || this.graphdbConfig.repositoryName
      if (!repoName) return

      this.graphdbLoading = true
      try {
        const response = await axios.post('/api/graphdb/count-triples', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryName: repoName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        this.graphdbStatusMessage = response.data.message
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to count triples'
      } finally {
        this.graphdbLoading = false
      }
    },

    confirmDeleteRepository(repositoryName) {
      this.repositoryToDelete = repositoryName
      if (!this.repositoryToDelete) return
      this.showDeleteConfirm = true
    },

    async deleteRepository() {
      this.graphdbLoading = true
      try {
        await axios.post('/api/graphdb/delete-repository', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryName: this.repositoryToDelete,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        })
        this.graphdbStatusMessage = `Repository '${this.repositoryToDelete}' deleted successfully`
        
        // Clear selection if we deleted the currently selected repository
        if (this.graphdbConfig.repositoryName === this.repositoryToDelete) {
          this.graphdbConfig.repositoryName = ''
        }
        
        this.showDeleteConfirm = false
        this.repositoryToDelete = ''
        await this.listRepositories()
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to delete repository'
        this.showDeleteConfirm = false
      } finally {
        this.graphdbLoading = false
      }
    },

    addCommonNamespace(commonNamespace) {
      // Check if this namespace prefix already exists
      const exists = this.formData.customNamespaces.some(ns => ns.prefix === commonNamespace.prefix)
      if (!exists) {
        this.formData.customNamespaces.push({ ...commonNamespace })
      }
    },

    handleImageError() {
      this.imageUrl = null
      console.error('Failed to load UML diagram image')
    },

    async loadImagePreview(file) {
      this.loadingImage = true
      this.imageUrl = null
      try {
        const response = await axios.get(`/api/rdf/preview/${file.id}`, {
          responseType: 'blob'
        })
        this.imageUrl = URL.createObjectURL(response.data)
      } catch (error) {
        console.error('Failed to load image preview:', error)
        this.imageUrl = null
      } finally {
        this.loadingImage = false
      }
    },

    selectAll() {
      this.uploadSelections.rdf = this.hasGeneratedData
      this.uploadSelections.shacl = this.formData.generateShacl
      this.uploadSelections.shex = this.formData.generateShex
      this.uploadSelections.namespaces = this.formData.enableCustomNamespaces
    },

    selectNone() {
      this.uploadSelections.rdf = false
      this.uploadSelections.shacl = false
      this.uploadSelections.shex = false
      this.uploadSelections.namespaces = false
    },

    async uploadSelected() {
      const uploads = []
      
      if (this.uploadSelections.rdf && this.hasGeneratedData) {
        uploads.push(this.uploadRDFGraph())
      }
      if (this.uploadSelections.shacl && this.formData.generateShacl) {
        uploads.push(this.uploadShaclPrefixes())
      }
      if (this.uploadSelections.shex && this.formData.generateShex) {
        uploads.push(this.uploadShexShapes())
      }
      if (this.uploadSelections.namespaces && this.formData.enableCustomNamespaces) {
        uploads.push(this.uploadCustomNamespaces())
      }

      if (uploads.length === 0) {
        this.graphdbErrorMessage = 'No items selected for upload'
        return
      }

      try {
        await Promise.all(uploads)
        this.graphdbStatusMessage = 'All selected items uploaded successfully'
      } catch (error) {
        console.error('Upload error:', error)
      }
    }

  }
}
function goBack() {
  router.push('/visualize&analysis')
}
</script>

<style scoped>
/* Add any component-specific styles here */
</style>