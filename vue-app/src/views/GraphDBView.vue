<template>
  <div class="graphdb-view-root min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="text-center">
          <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
            Graph Visualization and Analysis
          </h1>
          <p class="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
            Load your graph into GraphDB.
          </p>
        </div>

        <!-- Main Content Card -->
        <div class="mt-12 bg-white rounded-lg shadow-lg overflow-hidden">
          <div class="bg-gradient-to-r from-blue-600 to-blue-800 px-6 py-4">
            <h2 class="text-xl font-semibold text-white">Visualization in GraphDB</h2>
          </div>
          <div class="p-6">
          <!-- Custom Graph Name Input -->
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">Custom Graph Name</label>
            <input
              v-model="formData.graphName"
              @input="handleInput"
              type="text"
              placeholder="e.g. MyGraphDBGraph"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>

          <!-- Status Messages -->
          <div v-if="statusMessage" class="mb-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p class="text-green-800">{{ statusMessage }}</p>
          </div>
          <div v-if="errorMessage" class="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-800">{{ errorMessage }}</p>
          </div>

          <!-- Start Over Button -->
          <div v-if="hasGeneratedData" class="mb-6">
            <button
              @click="resetWorkflow"
              class="rounded-lg bg-gray-600 px-4 py-2 text-sm font-semibold text-white shadow-sm hover:bg-gray-500 focus:outline-none focus:ring-2 focus:ring-gray-400"
            >
              Start Over
            </button>
          </div>

          <!-- Step 1: Generate RDF Graph -->
          <div v-if="!hasGeneratedData" class="bg-gray-50 rounded-lg p-6 mb-6">
            <div class="flex items-center mb-4">
              <div class="bg-blue-100 p-2 rounded-lg mr-3">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900">Step 1: Generate RDF Graph</h3>

              
              
            </div>
              <div>
                An RDF Graph, its SHACL shapes, and ShEx shapes will be generated based on your input. You can also define custom namespaces and prefixes for the prefixes SHACL graph, which allows you to write SPARQL queries without needing to define the prefixes in the query editor.


              </div>
            
            <!-- Compact Form -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-4 pt-5">
              <!-- Left Column -->
              <div class="space-y-3">
                <input
                  type="url"
                  v-model="formData.baseUri"
                  placeholder="Base URI (e.g., https://biodatafuse.org/example/)"
                  class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <input
                  type="url"
                  v-model="formData.versionIri"
                  placeholder="Version IRI (e.g., https://biodatafuse.org/example/your_graph.ttl)"
                  class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <input
                  type="text"
                  v-model="formData.title"
                  placeholder="Graph Title (optional)"
                  class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <!-- Right Column -->
              <div class="space-y-3">
                <input
                  type="text"
                  v-model="formData.description"
                  placeholder="Graph Description (optional)"
                  class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <div class="flex items-center space-x-4">
                  <label class="flex items-center text-sm">
                    <input type="checkbox" v-model="formData.generateShacl" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-2">
                    SHACL
                  </label>
                  <label class="flex items-center text-sm">
                    <input type="checkbox" v-model="formData.generateShex" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-2">
                    ShEx
                  </label>
                  <label class="flex items-center text-sm">
                    <input type="checkbox" v-model="formData.generateUmlDiagram" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-2">
                    UML
                  </label>
                </div>
              </div>
            </div>

            <!-- Creators Section -->
            <div class="mb-4">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Creators <span class="text-gray-500">(Full Name and ORCID)</span>
              </label>
              <div class="space-y-2">
                <div v-for="(creator, index) in formData.creators" :key="index" class="flex gap-2">
                  <input
                    v-model="creator.fullName"
                    placeholder="Full Name"
                    class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                  <input
                    v-model="creator.orcid"
                    placeholder="ORCID (e.g., 0000-0000-0000-0000)"
                    class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                  <button 
                    v-if="formData.creators.length > 1"
                    @click="removeCreator(index)" 
                    class="text-red-500 hover:text-red-700 p-2"
                    title="Remove creator"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
                <button @click="addCreator" class="text-sm text-blue-600 hover:text-blue-800 inline-flex items-center">
                  <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                  </svg>
                  Add Creator
                </button>
              </div>
            </div>

            <!-- Custom Namespaces -->
            <div class="mb-4">
              <label class="flex items-center mb-3">
                <input type="checkbox" v-model="formData.enableCustomNamespaces" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500 mr-2">
                <span class="font-medium">Enable Custom Namespaces</span>
              </label>
              
              <div v-if="formData.enableCustomNamespaces" class="space-y-2">
                <div v-for="(namespace, index) in formData.customNamespaces" :key="index" class="flex gap-2">
                  <input
                    v-model="namespace.uri"
                    placeholder="URI"
                    class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                  <input
                    v-model="namespace.prefix"
                    placeholder="prefix"
                    class="flex-2 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  />
                  <button @click="removeNamespace(index)" class="text-red-500 hover:text-red-700 p-2">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
                <button @click="addNamespace" class="text-sm text-blue-600 hover:text-blue-800">
                  + Add Namespace
                </button>
              </div>
            </div>

            <!-- Generate Button -->
            <button
              @click="generateRDF"
              :disabled="loading || !isFormValid"
              class="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <span v-if="loading" class="animate-spin mr-2">◒</span>
              <span>{{ loading ? 'Generating...' : 'Generate RDF Graph' }}</span>
            </button>
          </div>

          <!-- Download Section -->
          <div v-if="hasGeneratedData" class="bg-gray-50 rounded-lg p-6 mb-6">
            <div class="flex items-center mb-4">
              <div class="bg-green-100 p-2 rounded-lg mr-3">
                <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <h3 class="text-lg font-semibold text-gray-900">Download Generated Files</h3>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <!-- Download RDF Graph -->
              <button
                @click="downloadSpecificFile('rdf')"
                class="inline-flex items-center border border-blue-500 px-4 py-2 text-sm font-semibold text-blue-700 rounded-lg hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-blue-400"
              >
                <svg class="w-4 h-4 mr-2 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                </svg>
                Download RDF Graph
              </button>

              <!-- Download SHACL Shapes -->
              <button
                v-if="formData.generateShacl"
                @click="downloadSpecificFile('shacl')"
                class="inline-flex items-center border border-purple-500 px-4 py-2 text-sm font-semibold text-purple-700 rounded-lg hover:bg-purple-50 focus:outline-none focus:ring-2 focus:ring-purple-400"
              >
                <svg class="w-4 h-4 mr-2 text-purple-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                </svg>
                Download SHACL Shapes
              </button>

              <!-- Download SHACL Prefixes -->
              <button
                v-if="formData.generateShacl"
                @click="downloadSpecificFile('shacl-prefixes')"
                class="inline-flex items-center border border-violet-500 px-4 py-2 text-sm font-semibold text-violet-700 rounded-lg hover:bg-violet-50 focus:outline-none focus:ring-2 focus:ring-violet-400"
              >
                <svg class="w-4 h-4 mr-2 text-violet-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                </svg>
                Download SHACL Prefixes
              </button>

              <!-- Download ShEx Shapes -->
              <button
                v-if="formData.generateShex"
                @click="downloadSpecificFile('shex')"
                class="inline-flex items-center border border-green-500 px-4 py-2 text-sm font-semibold text-green-700 rounded-lg hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-green-400"
              >
                <svg class="w-4 h-4 mr-2 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                </svg>
                Download ShEx Shapes
              </button>

              <!-- Download SHACL UML Preview -->
              <button
                v-if="formData.generateShacl && formData.generateUmlDiagram"
                @click="downloadSpecificFile('shacl-preview')"
                class="inline-flex items-center border border-indigo-500 px-4 py-2 text-sm font-semibold text-indigo-700 rounded-lg hover:bg-indigo-50 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              >
                <svg class="w-4 h-4 mr-2 text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                </svg>
                Download SHACL Preview
              </button>

              <!-- Download ShEx UML Preview -->
              <button
                v-if="formData.generateShex && formData.generateUmlDiagram"
                @click="downloadSpecificFile('shex-preview')"
                class="inline-flex items-center border border-teal-500 px-4 py-2 text-sm font-semibold text-teal-700 rounded-lg hover:bg-teal-50 focus:outline-none focus:ring-2 focus:ring-teal-400"
              >
                <svg class="w-4 h-4 mr-2 text-teal-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10l4 4m0 0l4-4m-4 4V3" />
                </svg>
                Download ShEx Preview
              </button>
            </div>
          </div>

          <!-- Schema Visualization -->
          <div v-if="hasGeneratedData && (formData.generateShacl || formData.generateShex)" class="bg-gray-50 rounded-lg p-6 mb-6">
            <h4 class="font-medium text-gray-900 mb-3">Schema Visualization</h4>
            <div class="flex space-x-4 mb-4">
              <button 
                v-if="formData.generateShacl" 
                @click="selectedVisualization = 'shacl'"
                :class="['px-3 py-2 text-sm rounded-lg border', selectedVisualization === 'shacl' ? 'bg-blue-50 border-blue-500 text-blue-700' : 'border-gray-300 text-gray-700 hover:bg-gray-50']"
              >
                SHACL Schema
              </button>
              <button 
                v-if="formData.generateShex" 
                @click="selectedVisualization = 'shex'"
                :class="['px-3 py-2 text-sm rounded-lg border', selectedVisualization === 'shex' ? 'bg-blue-50 border-blue-500 text-blue-700' : 'border-gray-300 text-gray-700 hover:bg-gray-50']"
              >
                ShEx Schema
              </button>
            </div>
            
            <div v-if="selectedVisualization && selectedUmlFile" class="bg-white rounded-lg border p-4">
              <div class="flex items-center justify-between mb-3">
                <h5 class="text-sm font-medium text-gray-900">
                  {{ selectedVisualization === 'shacl' ? 'SHACL' : 'ShEx' }} UML Diagram
                </h5>
                <button @click="downloadFile(selectedUmlFile)" class="text-blue-600 hover:text-blue-800 text-sm">
                  Download
                </button>
              </div>
              <div class="bg-white rounded border overflow-hidden">
                <div v-if="loadingImage" class="flex items-center justify-center p-8">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                  <span class="ml-3 text-gray-600">Loading diagram...</span>
                </div>
                <img 
                  v-else-if="imageUrl"
                  :src="imageUrl" 
                  :alt="`${selectedVisualization} UML Diagram`"
                  class="w-full h-auto object-contain"
                  style="max-height: 400px;"
                  @error="handleImageError"
                />
                <div v-else class="flex items-center justify-center p-8 text-gray-500">
                  <span>Diagram not available</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Manual Setup Instructions (Collapsible) -->
          <div class="bg-gray-50 rounded-lg p-4 mb-6">
            <button 
              @click="showManualSetup = !showManualSetup" 
              class="flex items-center w-full text-left text-blue-600 hover:text-blue-800 font-medium"
            >
              <svg :class="['w-5 h-5 mr-2 transition-transform', showManualSetup ? 'rotate-90' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
              Manual GraphDB Setup Instructions
            </button>
            
            <div v-if="showManualSetup" class="mt-4 prose prose-sm max-w-none">
              <div class="bg-white rounded-lg p-6 border">
                <h4 class="text-lg font-semibold text-gray-900 mb-4">Setting up GraphDB Locally</h4>
                
                <div class="space-y-6">
                  <div class="border-l-4 border-blue-500 pl-4">
                    <h5 class="font-semibold text-gray-900 mb-2">Step 1: Download and Install GraphDB</h5>
                    <ol class="list-decimal list-inside space-y-2 text-sm text-gray-700">
                      <li>Visit <a href="https://graphdb.ontotext.com/" target="_blank" class="text-blue-600 hover:text-blue-800 underline">https://graphdb.ontotext.com/</a></li>
                      <li>Click "Download GraphDB" and select the free version</li>
                      <li>Choose your operating system (Windows, macOS, or Linux)</li>
                      <li>Complete the registration form to download</li>
                      <li>Extract the downloaded file to your preferred location and install</li>
                    </ol>
                  </div>


                  <div class="border-l-4 border-purple-500 pl-4">
                    <h5 class="font-semibold text-gray-900 mb-2">Step 2: Access GraphDB Workbench</h5>
                    <ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
                      <li>Open your web browser</li>
                      <li>Navigate to <a href="http://localhost:7200" target="_blank" class="text-blue-600 hover:text-blue-800 underline font-mono">http://localhost:7200</a></li>
                      <li>You should see the GraphDB Workbench interface</li>
                    </ul>
                  </div>

                  <div class="border-l-4 border-orange-500 pl-4">
                    <h5 class="font-semibold text-gray-900 mb-2">Step 3: Create a Repository</h5>
                    <ol class="list-decimal list-inside space-y-1 text-sm text-gray-700">
                      <li>In the Workbench, click on "Setup" → "Repositories"</li>
                      <li>Click "Create new repository"</li>
                      <li>Choose "GraphDB Repository" as the type</li>
                      <li>Enter a repository ID (e.g., "biodatafuse-graph")</li>
                      <li>Optionally add a title and description</li>
                      <li>Click "Create" to finish</li>
                    </ol>
                  </div>

                  <div class="border-l-4 border-red-500 pl-4">
                    <h5 class="font-semibold text-gray-900 mb-2">Step 4: Import Your RDF Files</h5>
                    <ol class="list-decimal list-inside space-y-1 text-sm text-gray-700">
                      <li>Select your newly created repository from the repository dropdown</li>
                      <li>Go to "Import" → "RDF"</li>
                      <li>Choose "Upload RDF files"</li>
                      <li>
                        Click "Choose Files" and select your downloaded .ttl files:
                        <ul class="list-disc list-inside pl-4 space-y-1">
                          <li>Your graph ttl: your BioDataFuse query result in RDF</li>
                          <li>Your SHACL/ShEX shapes ttl: your BioDataFuse graph shapes for validation</li>
                          <li>Your SHACL prefixes ttl: your BioDataFuse graph prefixes to avoid having to state them in your SPARQL queries. Custom prefixes can be defined in the form above.</li>
                        </ul>
                      </li>
                      <li>Click "Import" to load the data</li>
                      <li>Wait for the import to complete</li>
                    </ol>
                  </div>

                  <div class="border-l-4 border-teal-500 pl-4">
                    <h5 class="font-semibold text-gray-900 mb-2">Step 6: Explore Your Data</h5>
                    <ul class="list-disc list-inside space-y-1 text-sm text-gray-700">
                      <li>Go to "SPARQL" to run queries against your data</li>
                      <li>Use "Explore" → "Visual graph" for interactive exploration</li>
                      <li>Try "Explore" → "Class relationships" to see your data structure</li>
                      <li>Use the search functionality to find specific entities</li>
                    </ul>
                  </div>
                </div>

                <div class="mt-6 p-4 bg-blue-50 rounded-lg">
                  <h6 class="font-semibold text-blue-900 mb-2">💡 Tips:</h6>
                  <ul class="list-disc list-inside space-y-1 text-sm text-blue-800">
                    <li>Start with a simple SPARQL query like: <code class="bg-blue-100 px-1 rounded">SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10</code></li>
                    <li>Check the "Namespaces" section to see all imported prefixes</li>
                    <li>Monitor memory usage if working with large datasets</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>

          <!-- GraphDB Connection (Collapsible) -->
          <div class="bg-gray-50 rounded-lg p-4 mb-6">
            <button 
              @click="showAdvancedOptions = !showAdvancedOptions" 
              class="flex items-center w-full text-left text-blue-600 hover:text-blue-800 font-medium"
            >
              <svg :class="['w-5 h-5 mr-2 transition-transform', showAdvancedOptions ? 'rotate-90' : '']" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
              Automated Upload to GraphDB Instance
            </button>
            
            <div v-if="showAdvancedOptions" class="mt-4 space-y-6">
              <!-- Step 2: GraphDB Setup -->
               <div v-if="!hasGeneratedData" class="bg-white rounded-lg p-6 border">
                Generate your RDF graph first to enable GraphDB setup.
               </div>
              <div v-if="hasGeneratedData" class="bg-white rounded-lg p-6 border">
                <div class="flex items-center mb-4">
                  <div class="bg-blue-100 p-2 rounded-lg mr-3">
                    <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"></path>
                    </svg>
                  </div>
                  <h3 class="text-lg font-semibold text-gray-900">GraphDB Connection</h3>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <!-- Connection Setup -->
                  <div class="space-y-4">
                    <!-- Connection Type -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-2">Connection Type</label>
                      <select v-model="connectionType" @change="updateUrlForConnectionType" class="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg">
                        <option value="docker">Docker Desktop (Windows, macOS)</option>
                        <option value="docker-bridge">Docker Bridge (Linux)</option>
                        <option value="local">Local (localhost:7200)</option>
                        <option value="remote">Remote Server</option>
                      </select>
                    </div>

                    <!-- GraphDB URL -->
                    <div>
                      <label class="block text-sm font-medium text-gray-700 mb-1">GraphDB URL</label>
                      <div class="flex gap-2">
                        <input
                          type="url"
                          v-model="graphdbConfig.baseUrl"
                          :placeholder="getUrlPlaceholder()"
                          class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg"
                        />
                        <button
                          @click="testConnection"
                          :disabled="!graphdbConfig.baseUrl || graphdbLoading"
                          class="px-3 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50"
                        >
                          {{ graphdbLoading ? 'Testing...' : 'Test' }}
                        </button>
                      </div>
                      <!-- Connection Status -->
                      <div v-if="connectionStatus" class="mt-2 text-sm">
                        <div v-if="connectionStatus.type === 'success'" class="text-green-600 flex items-center">
                          ✓ Connected successfully
                        </div>
                        <div v-else class="text-red-600">
                          ✗ {{ connectionStatus.message }}
                        </div>
                      </div>
                    </div>

                    <!-- Repository Management -->
                    <div v-if="connectionStatus?.type === 'success'">
                      <label class="block text-sm font-medium text-gray-700 mb-1">Repository</label>
                      <div class="flex gap-2 mb-2">
                        <input
                          type="text"
                          v-model="newRepositoryName"
                          placeholder="Repository name"
                          class="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg"
                        />
                        <button
                          @click="createRepository"
                          :disabled="graphdbLoading || !newRepositoryName.trim()"
                          class="px-3 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 disabled:opacity-50"
                        >
                          Create
                        </button>
                      </div>
                    </div>
                  </div>

                  <!-- Repository List -->
                  <div v-if="connectionStatus?.type === 'success'">
                    <div class="flex items-center justify-between mb-2">
                      <label class="block text-sm font-medium text-gray-700">Available Repositories</label>
                      <button 
                        @click="listRepositories" 
                        class="text-sm text-blue-600 hover:text-blue-800"
                      >
                        Refresh
                      </button>
                    </div>
                    <div class="bg-gray-50 rounded-lg max-h-48 overflow-y-auto">
                      <div v-if="repositories.length === 0" class="p-4 text-center text-gray-500 text-sm">
                        No repositories found
                      </div>
                      <div v-else class="divide-y divide-gray-200">
                        <div v-for="repo in repositories" :key="repo.id" 
                             :class="[
                               'p-3 cursor-pointer text-sm transition-colors',
                               graphdbConfig.repositoryName === repo.id ? 'bg-indigo-50 border-l-4 border-indigo-500' : 'hover:bg-white'
                             ]"
                             @click="selectRepository(repo.id)">
                          <div class="font-medium text-gray-900">{{ repo.id }}</div>
                          <div class="text-xs text-gray-500">{{ repo.title || 'No description' }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Step 3: Upload Data -->
              <div v-if="hasGeneratedData && graphdbConfig.repositoryName" class="bg-white rounded-lg p-6 border">
                <div class="flex items-center mb-4">
                  <div class="bg-purple-100 p-2 rounded-lg mr-3">
                    <svg class="w-5 h-5 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                    </svg>
                  </div>
                  <h3 class="text-lg font-semibold text-gray-900">Step 3: Upload to Repository: {{ graphdbConfig.repositoryName }}</h3>
                </div>

                <!-- Upload Options -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                    <input type="checkbox" v-model="uploadSelections.rdf" :disabled="!hasGeneratedData" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                    <div class="ml-3">
                      <div class="font-medium text-gray-900">RDF Graph</div>
                      <div class="text-sm text-gray-500">Core biological data</div>
                    </div>
                    <span v-if="uploadStatus.rdf === 'success'" class="ml-auto text-green-600 text-sm">✓</span>
                  </label>

                  <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer" :class="{ 'opacity-50': !formData.generateShacl }">
                    <input type="checkbox" v-model="uploadSelections.shacl" :disabled="!formData.generateShacl" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                    <div class="ml-3">
                      <div class="font-medium text-gray-900">SHACL Shapes</div>
                      <div class="text-sm text-gray-500">Data validation schemas</div>
                    </div>
                    <span v-if="uploadStatus.shacl === 'success'" class="ml-auto text-green-600 text-sm">✓</span>
                  </label>

                  <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer" :class="{ 'opacity-50': !formData.generateShacl }">
                    <input type="checkbox" v-model="uploadSelections.shaclPrefixes" :disabled="!formData.generateShacl" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                    <div class="ml-3">
                      <div class="font-medium text-gray-900">SHACL Prefixes</div>
                      <div class="text-sm text-gray-500">Namespace definitions</div>
                    </div>
                    <span v-if="uploadStatus.shaclPrefixes === 'success'" class="ml-auto text-green-600 text-sm">✓</span>
                  </label>

                  <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer" :class="{ 'opacity-50': !formData.generateShex }">
                    <input type="checkbox" v-model="uploadSelections.shex" :disabled="!formData.generateShex" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                    <div class="ml-3">
                      <div class="font-medium text-gray-900">ShEx Shapes</div>
                      <div class="text-sm text-gray-500">Shape expressions</div>
                    </div>
                    <span v-if="uploadStatus.shex === 'success'" class="ml-auto text-green-600 text-sm">✓</span>
                  </label>

                  <label class="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer" :class="{ 'opacity-50': !formData.enableCustomNamespaces }">
                    <input type="checkbox" v-model="uploadSelections.namespaces" :disabled="!formData.enableCustomNamespaces" class="rounded border-gray-300 text-blue-600 focus:ring-blue-500">
                    <div class="ml-3">
                      <div class="font-medium text-gray-900">Custom Namespaces</div>
                      <div class="text-sm text-gray-500">SPARQL prefixes</div>
                    </div>
                    <span v-if="uploadStatus.namespaces === 'success'" class="ml-auto text-green-600 text-sm">✓</span>
                  </label>
                </div>

                <!-- Upload Actions -->
                <div class="flex items-center justify-between">
                  <div class="flex space-x-4">
                    <button @click="selectAll" class="text-sm text-gray-600 hover:text-gray-800">Select All</button>
                    <button @click="selectNone" class="text-sm text-gray-600 hover:text-gray-800">Select None</button>
                  </div>
                  <button
                    @click="uploadSelected"
                    :disabled="!hasSelectedItems || isAnyUploading"
                    class="inline-flex items-center px-4 py-2 bg-blue-600 text-white font-semibold rounded-lg shadow hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                  >
                    <span v-if="isAnyUploading" class="animate-spin mr-2">◒</span>
                    <span>{{ isAnyUploading ? 'Uploading...' : 'Upload Selected' }}</span>
                  </button>
                </div>
              </div>

              <!-- Success Actions -->
              <div v-if="uploadStatus.rdf === 'success'" class="text-center">
                <button
                  @click="openGraphDBWorkbench"
                  class="inline-flex items-center px-6 py-3 bg-green-600 text-white font-semibold rounded-lg shadow hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  Open GraphDB Workbench
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer Actions -->
        <div class="flex justify-between px-6 py-4 bg-gray-50 border-t">
          <button
            type="button"
            @click="goBack"
            class="rounded-lg bg-white px-4 py-2 text-sm font-semibold text-gray-900 shadow-sm border border-gray-300 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-400"
          >
            ← Select another visualization tool
          </button>
        </div>
      </div> <!-- end main content card -->
    </div> <!-- end max width container -->

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
  </div> <!-- end graphdb view root -->
</template>

<script>
import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'GraphDBView',
  
  setup() {
    const authStore = useAuthStore()
    return { authStore }
  },

  data() {
    return {
      formData: {
        baseUri: 'https://biodatafuse.org/example/',
        versionIri: 'https://biodatafuse.org/example/your_graph.ttl',
        title: '',
        description: '',
        creators: [{ fullName: '', orcid: '' }],
        graphName: 'my_graph',
        generateShacl: true,
        shaclThreshold: 0.001,
        generateUmlDiagram: true,
        generateShex: true,
        shexThreshold: 0.001,
        enableCustomNamespaces: false,
        customNamespaces: []
      },
      generatedData: null,
      loading: false,
      errorMessage: '',
      statusMessage: '',
      graphdbConfig: {
        baseUrl: 'http://host.docker.internal:7200',
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
        rdf: null,
        shacl: null,
        shaclPrefixes: null,
        shex: null,
        namespaces: null
      },
      uploadSelections: {
        rdf: true,
        shacl: false,
        shaclPrefixes: false,
        shex: false,
        namespaces: false
      },
      connectionType: 'local',
      showAdvancedOptions: false,
      showManualSetup: false
    }
  },

  computed: {
    hasGeneratedData() {
      return this.generatedData && this.generatedData.generated_files && this.generatedData.generated_files.length > 0
    },
    isFormValid() {
      if (!this.formData.baseUri.trim() || 
          !this.formData.versionIri.trim() ||
          !this.formData.graphName.trim()) {
        return false
      }
      if (!this.formData.creators || this.formData.creators.length === 0) {
        return false
      }
      const firstCreator = this.formData.creators[0]
      return firstCreator.fullName.trim() && firstCreator.orcid.trim()
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
      if (this.formData.generateShacl && this.formData.generateUmlDiagram) {
        const shaclFile = this.generatedData.generated_files.find(file => 
          file.name === `${this.formData.graphName}_shacl.png`
        )
        if (shaclFile) return 'shacl'
      }
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

  mounted() {
    this.loadStoredData()
    if (this.selectedUmlFile) {
      this.loadImagePreview(this.selectedUmlFile)
    }
    if (this.defaultVisualization && !this.selectedVisualization) {
      this.selectedVisualization = this.defaultVisualization
    }
  },

  methods: {
    goBack() {
      window.location.href = '/visualize&analysis'
    },

    handleInput() {
      this.statusMessage = ''
      this.errorMessage = ''
    },

    async generateRDF() {
      if (!this.isFormValid) {
        this.errorMessage = 'Please fill in all required fields before generating the RDF graph.'
        return
      }
      this.loading = true
      this.errorMessage = ''
      this.statusMessage = ''
      try {
        const identifierSetId = localStorage.getItem('currentIdentifierSetId')
        if (!identifierSetId || isNaN(Number(identifierSetId))) {
          throw new Error('No valid identifier set found. Please complete the previous steps in the query builder.')
        }
        const creators = this.formData.creators
          .filter(creator => creator.fullName.trim() && creator.orcid.trim())
          .map(creator => ({
            full_name: creator.fullName.trim(),
            orcid: creator.orcid.trim().replace('https://orcid.org/', '')
          }))
        const response = await axios.post('/api/rdf/generate', {
          identifier_set_id: Number(identifierSetId),
          base_uri: this.formData.baseUri,
          version_iri: this.formData.versionIri,
          title: this.formData.title || null,
          description: this.formData.description || null,
          creators: creators,
          graph_name: this.formData.graphName,
          generate_shacl: this.formData.generateShacl,
          shacl_threshold: this.formData.shaclThreshold,
          generate_uml_diagram: this.formData.generateUmlDiagram,
          generate_shex: this.formData.generateShex,
          shex_threshold: this.formData.shexThreshold,
          custom_namespaces: this.formData.enableCustomNamespaces 
            ? this.formData.customNamespaces.filter(ns => ns.prefix && ns.uri)
            : null
        })
        this.generatedData = response.data
        localStorage.setItem('rdfGraphData', JSON.stringify(this.generatedData))
        this.statusMessage = 'RDF graph generated successfully!'
      } catch (error) {
        console.error('RDF generation error:', error)
        if (error.response) {
          const detail = error.response.data?.detail || error.response.data?.message || 'Unknown server error'
          this.errorMessage = `Server Error (${error.response.status}): ${detail}`
        } else if (error.request) {
          this.errorMessage = 'Network error: Could not connect to the server. Please check your internet connection and try again.'
        } else {
          this.errorMessage = error.message || 'Failed to generate RDF graph. Please try again.'
        }
      } finally {
        this.loading = false
      }
    },

    async testConnection() {
      this.connectionStatus = null
      this.graphdbLoading = true
      this.graphdbErrorMessage = ''
      this.graphdbStatusMessage = ''
      try {
        const requestData = {
          baseUrl: this.graphdbConfig.baseUrl,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null
        }
        const response = await axios.post('/api/graphdb/test-connection', requestData)
        console.log('✔ Frontend: Connection test successful:', response.data)
        this.connectionStatus = { type: 'success', message: response.data.message }
        await this.listRepositories()
      } catch (error) {
        console.error('❌ Frontend: Connection test failed:', error)
        if (error.response) {
          const errorMsg = error.response.data?.detail || 'Connection failed. Please check your settings.'
          this.connectionStatus = { type: 'error', message: errorMsg }
        } else if (error.request) {
          this.connectionStatus = { type: 'error', message: 'Network error - could not reach server' }
        } else {
          this.connectionStatus = { type: 'error', message: error.message }
        }
      } finally {
        this.graphdbLoading = false
      }
    },

    async uploadRDFGraph() {
      this.uploadingItems.add('rdf')
      this.uploadStatus.rdf = 'uploading'
      this.graphdbErrorMessage = ''
      try {
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
        const response = await axios.post('/api/graphdb/upload-rdf', payload)
        console.log('✔ RDF upload successful:', response.data)
        this.graphdbStatusMessage = response.data.message || 'RDF graph uploaded successfully'
        this.uploadStatus.rdf = 'success'
      } catch (error) {
        console.error('❌ RDF upload failed:', error)
        let errMsg = 'Failed to upload RDF graph'
        if (error.response) {
          const detail = error.response.data?.detail || error.response.data?.message
          errMsg = `Upload failed (${error.response.status}): ${detail || 'Unknown server error'}`
        } else if (error.request) {
          errMsg = 'Network error: Could not connect to upload service'
        } else {
          errMsg = error.message || errMsg
        }
        this.graphdbErrorMessage = errMsg
        this.uploadStatus.rdf = 'error'
      } finally {
        this.uploadingItems.delete('rdf')
      }
    },

    async uploadShaclPrefixes() {
      this.uploadingItems.add('shaclPrefixes')
      this.uploadStatus.shaclPrefixes = 'uploading'
      this.graphdbErrorMessage = ''
      try {
        const response = await axios.post('/api/graphdb/upload-shacl-prefixes', {
          baseUrl: this.graphdbConfig.baseUrl,
          repositoryId: this.graphdbConfig.repositoryName,
          username: this.graphdbConfig.username || null,
          password: this.graphdbConfig.password || null,
          graphData: this.generatedData
        })
        this.graphdbStatusMessage = response.data.message
        this.uploadStatus.shaclPrefixes = 'success'
      } catch (error) {
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to upload SHACL prefixes'
        this.uploadStatus.shaclPrefixes = 'error'
      } finally {
        this.uploadingItems.delete('shaclPrefixes')
      }
    },

    async uploadShaclShapes() {
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
      if (!this.graphdbConfig.baseUrl) return
      const workbenchUrl = `${this.graphdbConfig.baseUrl}/`
      window.open(workbenchUrl, '_blank')
    },

    resetWorkflow() {
      this.generatedData = null
      this.connectionStatus = null
      this.statusMessage = ''
      this.errorMessage = ''
      this.uploadingItems.clear()
      this.uploadStatus.rdf = null
      this.uploadStatus.shacl = null
      this.uploadStatus.shaclPrefixes = null
      this.uploadStatus.shex = null
      this.uploadStatus.namespaces = null
      this.graphdbConfig.repositoryName = ''
      localStorage.removeItem('rdfGraphData')
      this.selectedVisualization = ''
      if (this.imageUrl) {
        URL.revokeObjectURL(this.imageUrl)
        this.imageUrl = null
      }
    },

    loadStoredData() {
      const storedData = localStorage.getItem('rdfGraphData')
      if (storedData) {
        try {
          this.generatedData = JSON.parse(storedData)
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

    addCreator() {
      this.formData.creators.push({ fullName: '', orcid: '' })
    },

    removeCreator(index) {
      if (this.formData.creators.length > 1) {
        this.formData.creators.splice(index, 1)
      }
    },

    selectRepository(repositoryId) {
      this.graphdbConfig.repositoryName = repositoryId
    },

    async downloadSpecificFile(fileType) {
      if (!this.generatedData?.generation_id) {
        this.errorMessage = 'No generation ID found. Please generate RDF first.'
        return
      }
      try {
        const endpoint = `/api/rdf/download-${fileType}/${this.generatedData.generation_id}`
        const response = await axios.get(endpoint, {
          responseType: 'blob',
          headers: this.authStore?.token
            ? { Authorization: `Bearer ${this.authStore.token}` }
            : {}
        })
        const url = URL.createObjectURL(response.data)
        const a = document.createElement('a')
        a.href = url
        const contentDisposition = response.headers['content-disposition']
        let filename = `${fileType}_${this.generatedData.graph_name}`
        if (contentDisposition) {
          const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
          if (filenameMatch && filenameMatch[1]) {
            filename = filenameMatch[1].replace(/['"]/g, '')
          }
        } else {
          if (fileType.includes('preview')) {
            filename += '.png'
          } else if (fileType === 'shex') {
            filename += '.shex'
          } else {
            filename += '.ttl'
          }
        }
        a.download = filename
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
        this.statusMessage = `${fileType} file downloaded successfully!`
      } catch (error) {
        console.error(`Error downloading ${fileType} file:`, error)
        if (error.response?.status === 404) {
          this.errorMessage = `${fileType} file not found. Make sure the file was generated.`
        } else if (error.response?.status === 401) {
          this.errorMessage = 'Authentication failed. Please log in again.'
        } else {
          this.errorMessage = `Failed to download ${fileType} file. Please try again.`
        }
      }
    },

    async downloadFile(file) {
      try {
        const response = await axios.get(`/api/rdf/download/${file.id}`, {
          responseType: 'blob',
          headers: this.authStore?.token
            ? { Authorization: `Bearer ${this.authStore.token}` }
            : {}
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
        console.error('Error downloading file:', error)
        this.errorMessage = 'Failed to download file'
      }
    },

    async listRepositories() {
      if (!this.graphdbConfig.baseUrl) {
        console.warn('No GraphDB URL provided for listing repositories')
        return
      }
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
        this.graphdbErrorMessage = error.response?.data?.detail || 'Failed to fetch repositories'
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
        this.newRepositoryName = ''
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
      const exists = this.formData.customNamespaces.some(ns => ns.prefix === commonNamespace.prefix)
      if (!exists) {
        this.formData.customNamespaces.push({ ...commonNamespace })
      }
    },

    handleImageError() {
      if (this.imageUrl) {
        URL.revokeObjectURL(this.imageUrl)
      }
      this.imageUrl = null
      console.error('Failed to load UML diagram image')
    },

    async loadImagePreview(file) {
      this.loadingImage = true
      if (this.imageUrl) {
        URL.revokeObjectURL(this.imageUrl)
        this.imageUrl = null
      }
      try {
        const response = await axios.get(`/api/rdf/preview/${file.id}`, {
          responseType: 'blob',
          headers: this.authStore?.token
            ? { Authorization: `Bearer ${this.authStore.token}` }
            : {}
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
      this.uploadSelections.shaclPrefixes = this.formData.generateShacl
      this.uploadSelections.shex = this.formData.generateShex
      this.uploadSelections.namespaces = this.formData.enableCustomNamespaces
    },

    selectNone() {
      this.uploadSelections.rdf = false
      this.uploadSelections.shacl = false
      this.uploadSelections.shaclPrefixes = false
      this.uploadSelections.shex = false
      this.uploadSelections.namespaces = false
    },

    async uploadSelected() {
      const uploads = []
      if (this.uploadSelections.rdf && this.hasGeneratedData) {
        uploads.push(this.uploadRDFGraph())
      }
      if (this.uploadSelections.shacl && this.formData.generateShacl) {
        uploads.push(this.uploadShaclShapes())
      }
      if (this.uploadSelections.shaclPrefixes && this.formData.generateShacl) {
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
    },

    updateUrlForConnectionType() {
      switch (this.connectionType) {
        case 'local':
          this.graphdbConfig.baseUrl = 'http://localhost:7200'
          break
        case 'docker':
          this.graphdbConfig.baseUrl = 'http://host.docker.internal:7200'
          break
        case 'docker-bridge':
          this.graphdbConfig.baseUrl = 'http://172.17.0.1:7200'
          break
        case 'remote':
          this.graphdbConfig.baseUrl = 'https://'
          break
      }
    },

    getUrlPlaceholder() {
      switch (this.connectionType) {
        case 'local':
          return 'http://localhost:7200'
        case 'docker':
          return 'http://host.docker.internal:7200'
        case 'docker-bridge':
          return 'http://172.17.0.1:7200'
        case 'remote':
          return 'https://your-graphdb-server.com:7200'
        default:
          return 'GraphDB URL'
      }
    },

    getConnectionTypeHint() {
      switch (this.connectionType) {
        case 'local':
          return 'Use localhost when both this app and GraphDB are running directly on your computer'
        case 'docker':
          return 'Use host.docker.internal for Docker Desktop on Mac/Windows bridge network'
        case 'docker-bridge':
          return 'Use 172.17.0.1 for Linux Docker default bridge network'
        case 'remote':
          return 'Use the full URL including protocol (http:// or https://) for remote GraphDB instances'
        default:
          return ''
      }
    }
  }
}
</script>
