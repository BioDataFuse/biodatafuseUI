<template>
  <div class="bg-white py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 class="text-3xl font-extrabold text-gray-900 mb-4">Contact & Contributors</h2>
      <p class="text-lg text-gray-600 mb-4 max-w-3xl">
        pyBioDataFuse is developed as part of the Elixir BioHackathon 2023, with contributions from multiple ELIXIR nodes.
      </p>
      <p class="text-lg text-gray-600 mb-4 max-w-3xl">
        For questions, feedback, or contributions, please visit our GitHub repository:
      </p>
      <a
        href="https://github.com/BioDataFuse/pyBiodatafuse"
        class="text-indigo-600 hover:underline text-lg"
        target="_blank"
      >
        https://github.com/BioDataFuse/pyBiodatafuse
      </a>
    </div>
  </div>

  
        <div class="bg-gray-50 rounded-lg p-6 shadow mt-12">
        <h3 class="text-xl font-semibold text-indigo-700 mb-2">
          Post-COVID Syndrome (PCS) Workflow Notebook
        </h3>
        <p class="text-gray-700 mb-4">
          This advanced use case demonstrates how to construct a knowledge graph for Post-COVID Syndrome (PCS),
          integrating multi-source biological data and enabling downstream RDF and graph database exports.
        </p>

        <!-- Toggle Button -->
        <button
          @click="showSteps = !showSteps"
          class="mb-4 inline-flex items-center text-indigo-600 font-medium hover:underline focus:outline-none"
        >
          {{ showSteps ? 'Hide Details ▲' : 'Show Workflow Steps ▼' }}
        </button>
        <br>  
        <!-- Workflow Steps (Hidden by default) -->
        <Transition name="fade">
          <ul
            v-if="showSteps"
            class="list-disc list-inside text-gray-700 space-y-1 ml-4"
          >
            <li v-for="(step, index) in steps" :key="index">{{ step }}</li>
          </ul>
        </Transition>

        <!-- Notebook Link -->
        <router-link
          to="https://github.com/BioDataFuse/pyBiodatafuse/blob/main/examples/usecases/PCS/PCS.ipynb"
          target="_blank"
          class="mt-4 inline-flex items-center justify-center px-5 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
        >
          View Notebook on GitHub
        </router-link>
      </div>
</template>
