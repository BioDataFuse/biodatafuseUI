<template>
  <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
    <div class="px-4 py-6 sm:px-0">
      <div class="max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold text-gray-900">About BioDataFuse</h1>
        
        <div class="mt-6 prose prose-indigo">
          <p class="text-lg text-gray-500">
            BioDataFuse is a comprehensive platform for integrating and analyzing biological data from multiple sources. 
            Our platform helps researchers discover new insights by connecting different types of biological data.
          </p>

          <h2 class="mt-8 text-2xl font-bold text-gray-900">Key Features</h2>
          
          <div class="mt-6 grid gap-6 lg:grid-cols-2">
            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg font-medium text-gray-900">Data Integration</h3>
                <p class="mt-2 text-gray-500">
                  Connect and analyze data from multiple biological databases seamlessly.
                </p>
              </div>
            </div>

            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg font-medium text-gray-900">Advanced Analysis</h3>
                <p class="mt-2 text-gray-500">
                  Perform sophisticated analyses with our comprehensive suite of tools.
                </p>
              </div>
            </div>

            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg font-medium text-gray-900">Visualization</h3>
                <p class="mt-2 text-gray-500">
                  Create interactive visualizations of your data and results.
                </p>
              </div>
            </div>

            <div class="bg-white overflow-hidden shadow rounded-lg">
              <div class="px-4 py-5 sm:p-6">
                <h3 class="text-lg font-medium text-gray-900">API Access</h3>
                <p class="mt-2 text-gray-500">
                  Programmatic access to all platform features through our REST API.
                </p>
              </div>
            </div>
          </div>

          <h2 class="mt-12 text-2xl font-bold text-gray-900">Supported Databases</h2>
          
          <div class="mt-6 space-y-4">
            <div v-for="db in databases" :key="db.id" class="bg-white overflow-hidden shadow rounded-lg">
              <div class="px-4 py-5 sm:p-6">
                <div class="flex items-center">
                  <div class="flex items-center justify-center h-12 w-12 rounded-md bg-indigo-100 text-indigo-600">
                    <component :is="db.icon" class="h-6 w-6" />
                  </div>
                  <div class="ml-4">
                    <h3 class="text-lg font-medium text-gray-900">{{ db.name }}</h3>
                    <p class="mt-1 text-gray-500">{{ db.description }}</p>
                    <div class="mt-2">
                      <a 
                        :href="db.url" 
                        target="_blank" 
                        rel="noopener"
                        class="text-indigo-600 hover:text-indigo-900 text-sm font-medium"
                      >
                        Learn more →
                      </a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <h2 class="mt-12 text-2xl font-bold text-gray-900">Contact Us</h2>
          
          <div class="mt-6 bg-white overflow-hidden shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <div class="grid grid-cols-1 gap-6">
                <div>
                  <h3 class="text-lg font-medium text-gray-900">Support</h3>
                  <p class="mt-2 text-gray-500">
                    Need help? Contact our support team at 
                    <a href="mailto:support@biodatafuse.com" class="text-indigo-600 hover:text-indigo-900">
                      support@biodatafuse.com
                    </a>
                  </p>
                </div>
                <div>
                  <h3 class="text-lg font-medium text-gray-900">Documentation</h3>
                  <p class="mt-2 text-gray-500">
                    Visit our 
                    <a href="#" class="text-indigo-600 hover:text-indigo-900">
                      documentation
                    </a>
                    for detailed guides and API references.
                  </p>
                </div>
                <div>
                  <h3 class="text-lg font-medium text-gray-900">Community</h3>
                  <p class="mt-2 text-gray-500">
                    Join our community on 
                    <a href="#" class="text-indigo-600 hover:text-indigo-900">
                      GitHub
                    </a>
                    to contribute and stay updated.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  BeakerIcon,
  CircleStackIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'

const databases = [
  {
    id: 'disgenet',
    name: 'DisGeNET',
    description: 'Database of gene-disease associations integrating data from various expert curated databases and text-mining derived associations.',
    icon: BeakerIcon,
    url: 'https://www.disgenet.org/'
  },
  {
    id: 'string',
    name: 'STRING',
    description: 'Database of known and predicted protein-protein interactions, including direct (physical) and indirect (functional) associations.',
    icon: CircleStackIcon,
    url: 'https://string-db.org/'
  },
  {
    id: 'reactome',
    name: 'Reactome',
    description: 'Free, open-source, curated and peer-reviewed pathway database providing visualization, interpretation and analysis of pathway knowledge.',
    icon: ChartBarIcon,
    url: 'https://reactome.org/'
  }
]
</script>