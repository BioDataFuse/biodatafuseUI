<template>
  <div class="bg-white shadow rounded-md p-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Filters</h3>
    
    <!-- Data Source Filters -->
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700">Data Sources</label>
        <div class="mt-2 space-y-2">
          <div v-for="source in dataSources" :key="source" class="flex items-center">
            <input
              :id="source"
              type="checkbox"
              v-model="selectedSources[source]"
              class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              @change="emitChanges"
            />
            <label :for="source" class="ml-2 text-sm text-gray-700">{{ source }}</label>
          </div>
        </div>
      </div>

      <!-- Edge Weight Filter -->
      <div>
        <label class="block text-sm font-medium text-gray-700">
          Edge Weight Threshold: {{ edgeWeightThreshold }}
        </label>
        <input
          type="range"
          v-model="edgeWeightThreshold"
          min="0"
          max="1"
          step="0.1"
          class="mt-2 w-full"
          @input="emitChanges"
        />
        <div class="mt-1 flex justify-between text-xs text-gray-500">
          <span>0</span>
          <span>0.5</span>
          <span>1</span>
        </div>
      </div>

      <!-- Node Type Filters -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Node Types</label>
        <div class="mt-2 space-y-2">
          <div v-for="type in nodeTypes" :key="type" class="flex items-center">
            <input
              :id="'node-' + type"
              type="checkbox"
              v-model="selectedNodeTypes[type]"
              class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
              @change="emitChanges"
            />
            <label :for="'node-' + type" class="ml-2 text-sm text-gray-700">
              <span
                class="inline-block w-3 h-3 rounded-full mr-1"
                :style="{ backgroundColor: nodeColors[type] }"
              ></span>
              {{ type }}
            </label>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

const props = defineProps<{
  dataSources: string[]
  nodeTypes: string[]
  nodeColors: Record<string, string>
}>()

const emit = defineEmits<{
  (e: 'update', filters: {
    sources: Record<string, boolean>
    nodeTypes: Record<string, boolean>
    edgeWeight: number
  }): void
}>()

const selectedSources = reactive(
  Object.fromEntries(props.dataSources.map(source => [source, true]))
)

const selectedNodeTypes = reactive(
  Object.fromEntries(props.nodeTypes.map(type => [type, true]))
)

const edgeWeightThreshold = ref(0.5)

function emitChanges() {
  emit('update', {
    sources: selectedSources,
    nodeTypes: selectedNodeTypes,
    edgeWeight: edgeWeightThreshold.value
  })
}
</script>