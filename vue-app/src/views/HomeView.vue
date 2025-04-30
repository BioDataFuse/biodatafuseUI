<template>
  <div class="bg-white">
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <div class="max-w-7xl mx-auto">
        <div class="relative z-10 pb-8 bg-white sm:pb-16 md:pb-20 lg:w-full lg:pb-28 xl:pb-32">
          <main class="mt-10 mx-auto max-w-7xl px-4 sm:mt-12 sm:px-6 lg:mt-16 lg:px-8 xl:mt-28">
            <div class="sm:text-center lg:text-left">
              <h1 class="text-4xl tracking-tight font-extrabold text-gray-900 sm:text-5xl md:text-6xl">
                <span class="block">Advanced Bioinformatics</span>
                <span class="block text-indigo-600">Data Integration Platform</span>
              </h1>
              <p class="mt-3 text-base text-gray-500 sm:mt-5 sm:text-lg sm:max-w-xl sm:mx-auto md:mt-5 md:text-xl lg:mx-0">
                Integrate and analyze complex biological data from multiple sources. Discover new insights and relationships in your research data.
              </p>
              <div class="mt-5 sm:mt-8 sm:flex sm:justify-center lg:justify-start">
                <div class="rounded-md shadow">
                  <router-link
                    to="/query"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 md:py-4 md:text-lg md:px-10"
                  >
                    Start Analysis
                  </router-link>
                </div>
                <div class="mt-3 sm:mt-0 sm:ml-3">
                  <router-link
                    to="/about"
                    class="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 md:py-4 md:text-lg md:px-10"
                  >
                    Learn More
                  </router-link>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </div>

    <!-- Feature Section -->
    <div class="py-12 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-indigo-600 font-semibold tracking-wide uppercase">Features</h2>
          <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Better Data Integration
          </p>
          <p class="mt-4 max-w-2xl text-xl text-gray-500 lg:mx-auto">
            Comprehensive tools for biological data analysis and integration.
          </p>
        </div>

        <div class="mt-10">
          <dl class="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
            <div v-for="feature in features" :key="feature.name" class="relative">
              <dt>
                <div class="absolute flex items-center justify-center h-12 w-12 rounded-md bg-indigo-500 text-white">
                  <component :is="feature.icon" class="h-6 w-6" aria-hidden="true" />
                </div>
                <p class="ml-16 text-lg leading-6 font-medium text-gray-900">{{ feature.name }}</p>
              </dt>
              <dd class="mt-2 ml-16 text-base text-gray-500">{{ feature.description }}</dd>
            </div>
          </dl>
        </div>
      </div>
    </div>

    <!-- Database Section -->
    <div class="bg-gray-50 py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="lg:text-center">
          <h2 class="text-base text-indigo-600 font-semibold tracking-wide uppercase">Supported Databases</h2>
          <p class="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 sm:text-4xl">
            Comprehensive Data Sources
          </p>
        </div>

        <div class="mt-10">
          <div class="space-y-10 md:space-y-0 md:grid md:grid-cols-3 md:gap-x-8 md:gap-y-10">
            <div v-for="db in databases" :key="db.name" class="relative bg-white p-6 rounded-lg shadow">
              <h3 class="text-lg font-medium text-gray-900">{{ db.name }}</h3>
              <p class="mt-2 text-base text-gray-500">{{ db.description }}</p>
              <div class="mt-4">
                <span class="inline-flex items-center px-3 py-0.5 rounded-full text-sm font-medium" :class="db.tagClass">
                  {{ db.type }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistics Section -->
    <div class="bg-white py-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <dl class="rounded-lg bg-white shadow-lg sm:grid sm:grid-cols-3">
          <div v-for="stat in stats" :key="stat.name" class="flex flex-col border-b border-gray-100 p-6 text-center sm:border-0 sm:border-r">
            <dt class="order-2 mt-2 text-lg font-medium text-gray-500">{{ stat.name }}</dt>
            <dd class="order-1 text-5xl font-extrabold text-indigo-600">{{ stat.value }}</dd>
          </div>
        </dl>
      </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-indigo-50">
      <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8 lg:flex lg:items-center lg:justify-between">
        <h2 class="text-3xl font-extrabold tracking-tight text-gray-900 sm:text-4xl">
          <span class="block">Ready to dive in?</span>
          <span class="block text-indigo-600">Start your analysis today.</span>
        </h2>
        <div class="mt-8 flex lg:mt-0 lg:flex-shrink-0">
          <div class="inline-flex rounded-md shadow">
            <router-link
              to="/register"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
            >
              Get Started
            </router-link>
          </div>
          <div class="ml-3 inline-flex rounded-md shadow">
            <router-link
              to="/about"
              class="inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-indigo-600 bg-white hover:bg-indigo-50"
            >
              Learn More
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {
  Squares2X2Icon,
  BeakerIcon,
  CircleStackIcon,
  LightBulbIcon
} from '@heroicons/vue/24/outline'

const features = [
  {
    name: 'Data Integration',
    description: 'Connect and analyze data from multiple biological databases seamlessly.',
    icon: CircleStackIcon
  },
  {
    name: 'Advanced Analytics',
    description: 'Powerful tools for statistical analysis and data visualization.',
    icon: Squares2X2Icon
  },
  {
    name: 'Network Analysis',
    description: 'Explore and visualize biological networks and pathways.',
    icon: BeakerIcon
  },
  // {
  //   name: 'Smart Insights',
  //   description: 'AI-powered analysis to discover hidden patterns in your data.',
  //   icon: LightBulbIcon
  // }
]

const databases = [
  {
    name: 'DisGeNET',
    description: 'Gene-disease associations database with comprehensive coverage of human diseases.',
    type: 'Genomics',
    tagClass: 'bg-green-100 text-green-800'
  },
  {
    name: 'STRING',
    description: 'Protein-protein interaction networks for functional enrichment analysis.',
    type: 'Proteomics',
    tagClass: 'bg-blue-100 text-blue-800'
  },
  {
    name: 'Reactome',
    description: 'Curated pathways database for understanding biological processes.',
    type: 'Pathways',
    tagClass: 'bg-purple-100 text-purple-800'
  }
]

// const stats = [
//   { name: 'Databases Integrated', value: '20+' },
//   { name: 'Research Papers', value: '1000+' },
//   { name: 'Active Users', value: '5000+' }
// ]
</script>