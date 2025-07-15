<template>
  <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Intro -->
      <div class="mt-10 space-y-6 text-base text-gray-500 leading-relaxed">
        <p>
          <strong class="text-gray-900">BioDataFuse</strong> is an open-source platform designed to streamline the integration and contextual analysis of diverse biomedical data sources. It provides a modular query-based system that allows users to build tailored <strong class="text-gray-900">knowledge graphs</strong> from heterogeneous data inputs.
        </p>
        <p>
          At its core, BioDataFuse leverages the power of its Python package, <a href="https://github.com/BioDataFuse/pyBiodatafuse" target="_blank" class="text-indigo-600 hover:text-indigo-800 font-medium">pyBiodatafuse</a>, which aggregates and harmonizes biological data from supported databases. It integrates seamlessly with tools like Neo4j and Cytoscape, supporting local graph hosting and advanced network analysis.
        </p>
        <p>
          These knowledge graphs can be dynamically generated based on user-defined queries, facilitating applications such as target discovery, disease mechanism exploration, and drug repurposing.
        </p>
      </div>

      <!-- Key Capabilities -->
      <div class="mt-12">
        <h2 class="text-2xl font-bold text-gray-900">Key Capabilities</h2>
        <ul class="mt-4 space-y-2 text-base text-gray-500 list-disc list-inside">
          <li>Modular integration of heterogeneous biological datasets</li>
          <li>Real-time construction of user-defined knowledge graphs</li>
          <li>Built-in compatibility with Cytoscape and Neo4j</li>
          <li>Graph analytics support, including link prediction</li>
          <li>Designed following FAIR principles for data reuse and transparency</li>
        </ul>
      </div>


      <!-- Collaboration & Interoperability -->
      <div class="mt-12">
        <h2 class="text-2xl font-bold text-gray-900">Collaboration & Interoperability Focus</h2>
        <p class="mt-4 text-base text-gray-500">
          BioDataFuse is the result of a collaborative effort among several European academic and research institutions. The project reflects a shared commitment to improving biomedical data interoperability and harmonization, aligning with priorities set by the ELIXIR Interoperability Platform.
        </p>
      </div>

      <!-- Open Source -->
      <div class="mt-12">
        <h2 class="text-2xl font-bold text-gray-900">Open Source & UI Access</h2>
        <p class="mt-4 text-base text-gray-500">
          The project is fully open-source and community-driven. You can explore and contribute to the core packages:
        </p>
        <div class="mt-6 flex flex-wrap gap-4">
          <a
            href="https://github.com/BioDataFuse/pyBiodatafuse"
            target="_blank"
            class="inline-block px-6 py-3 bg-indigo-600 text-white font-medium rounded-md hover:bg-indigo-700"
          >
            pyBiodatafuse (Python Backend)
          </a>
          <a
            href="https://github.com/BioDataFuse/biodatafuseUI"
            target="_blank"
            class="inline-block px-6 py-3 bg-indigo-100 text-indigo-700 font-medium rounded-md hover:bg-indigo-200"
          >
            biodatafuseUI (Web Interface)
          </a>
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