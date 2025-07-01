<template>
  <div class="min-h-screen bg-gradient-to-b from-gray-50 to-white">
    <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <!-- Header -->
      <div class="text-center">
        <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl">
          Graph Visualization and Analysis
        </h1>
        <p class="mt-4 text-xl text-gray-600 max-w-2xl mx-auto">
          Load your graph into Neo4j database.
        </p>
      </div>

      <!-- Tab Bar -->
      <div class="mt-12 bg-white rounded-2xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-800 px-6 py-4">
          <div class="flex space-x-8">
            <div
              @click="selectedTab = 'visualization'"
              class="pb-2 text-xl font-medium focus:outline-none cursor-pointer"
            >
              <h2 class="text-xl font-semibold text-white">Visualization in Neo4j</h2>
            </div>
          </div>
        </div>
      </div>

      <!-- Instructions + Form -->
      <div class="from-indigo-600 to-indigo-800 px-6 py-4">
        <div class="mt-1 text-black text-xl">
          <p class="text-xl text-gray-600 mb-6">
            <strong>Instructions:</strong><br><br>
            • Ensure your <strong>Neo4j database</strong> is running and accessible.<br>
            <button @click="showNeo4jHelp = !showNeo4jHelp" class="ml-2 text-indigo-600 underline text-sm focus:outline-none">
              {{ showNeo4jHelp ? 'Hide details' : 'More info' }}
            </button>
            <transition name="fade">
              <div v-if="showNeo4jHelp" class="mt-2 text-gray-500 text-base border-l-4 border-indigo-200 pl-4 space-y-2">
                <p class="font-semibold">To connect to Neo4j, make sure the following are in place:</p>
                <ul class="list-disc list-inside">
                  <li>Install Neo4j Desktop or Server if not already installed.</li>
                  <li>Add or open a local <strong>DBMS</strong> instance.</li>
                  <li>Start the DBMS and open <strong>Neo4j Browser</strong> for that DBMS.</li>
                  <li>In the left panel, go to <strong>Database</strong> to verify it is running.</li>
                </ul>
                
                <p class="font-semibold">User setup:</p>
                <ul class="list-disc list-inside">
                  <li>Click the <code>:server user add</code> command or go to settings to create a new user.</li>
                  <li>Assign the user a password and set their role to <code>admin</code>.</li>
                  <li>Use the same username and password in this interface.</li>
                </ul>

                <p class="font-semibold">Common error fix:</p>
                <p>
                  If you receive this error:
                  <br>
                  <code class="text-sm text-red-600 block mt-1">
                    500: Error loading graph into Neo4j: {code: Neo.ClientError.Security.Unauthorized} {message: The client is unauthorized due to authentication failure.}
                  </code>
                  Then:
                </p>
                <ul class="list-disc list-inside">
                  <li>Go to the DBMS settings (click the <code>⋮</code> menu for the DBMS and choose <strong>Settings</strong>).</li>
                  <li>Edit the config file and set:
                    <br>
                    <code class="text-sm block bg-gray-100 p-2 mt-1 rounded">
                      dbms.security.auth_enabled=false
                    </code>
                    <span class="text-sm italic text-gray-500">Note: this disables authentication, which should only be used in a local/trusted setup.</span>
                  </li>
                </ul>
                <p>
                  After making changes, restart the DBMS to apply the new settings.
                </p>
              </div>
            </transition>

          </p>
          <p class="text-xl text-gray-600 mb-6">
            • Provide a valid connection URI, username, and password.<br>
            • Process your data before visualizing it.<br>
            • If the graph has no edges, it will not be loaded.
          </p>

          <div class="space-y-4">
            <div class="mb-6">
              <label class="block text-gray-700 font-medium mb-2">Neo4j URI</label>
              <input
                v-model="uri"
                type="text"
                placeholder="bolt://localhost:7687"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200"
              />
            </div>

            <div class="mb-6">
              <label class="block text-gray-700 font-medium mb-2">Username</label>
              <input 
                v-model="username"
                type="text"
                placeholder="neo4j"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200"
              />
            </div>

            <div class="mb-6">
              <label class="block text-gray-700 font-medium mb-2">Password</label>
              <input 
                v-model="password"
                type="password"
                class="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200"
              />
            </div>
          </div>
        </div>
        
        <!-- Footer Actions -->
        <div class="mt-8 flex justify-between px-6 py-4 bg-white rounded-b-xl shadow-lg">
          <button
            @click="goBack"
            class="px-4 py-2 border border-indigo-600 text-indigo-600 font-semibold rounded-lg hover:bg-indigo-100"
          >
            ← Select another visualization tool
          </button>
          <button
            @click="loadNeo4jGraph"
            :disabled="loading"
            class="inline-flex items-center px-4 py-2 bg-indigo-600 text-white font-semibold rounded-lg shadow hover:bg-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          >
            <span v-if="loading" class="animate-spin mr-2">🔄</span>
            <span>{{ loading ? 'Loading...' : 'Load your graph into Neo4j' }}</span>
          </button>
        </div>
        <p v-if="statusMessage" class="mt-6 text-lg text-green-600">{{ statusMessage }}</p>
        <p v-if="errorMessage" class="mt-6 text-lg text-red-600">{{ errorMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const uri = ref('bolt://localhost:7687')
const username = ref('neo4j')
const password = ref('password')

const statusMessage = ref('')
const errorMessage = ref('')
const loading = ref(false)
const identifierSetId = localStorage.getItem('currentIdentifierSetId')
const showNeo4jHelp = ref(false)

const loadNeo4jGraph = async () => {
  statusMessage.value = ''
  errorMessage.value = ''

  if (!identifierSetId) {
    errorMessage.value = 'No identifier set selected. Please process your data first.'
    return
  }

  if (!uri.value || !username.value || !password.value) {
    errorMessage.value = 'Please fill in all connection details.'
    return
  }

  loading.value = true
  try {
    const response = await axios.post(`/api/visualize&analysis/neo4j/${identifierSetId}`, {
      uri: uri.value,
      username: username.value,
      password: password.value
    })
    statusMessage.value = response.data.message
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || 'Failed to connect to Neo4j.'
  } finally {
    loading.value = false
  }
}
function goBack() {
  router.push('/visualize&analysis')
}
</script>
