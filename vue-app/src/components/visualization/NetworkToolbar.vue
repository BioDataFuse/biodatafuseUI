<template>
  <div class="bg-white shadow rounded-md p-4">
    <div class="space-y-4">
      <!-- Layout Controls -->
      <div>
        <label class="block text-sm font-medium text-gray-700">Layout</label>
        <select
          v-model="selectedLayout"
          class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 rounded-md"
          @change="$emit('layout-change', selectedLayout)"
        >
          <option value="force">Force-Directed</option>
          <option value="circular">Circular</option>
          <option value="concentric">Concentric</option>
          <option value="grid">Grid</option>
        </select>
      </div>

      <!-- Zoom Controls -->
      <div class="flex space-x-2">
        <button
          v-for="(icon, action) in zoomControls"
          :key="action"
          @click="$emit('zoom', action)"
          class="inline-flex items-center p-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
          :title="action"
        >
          <component :is="icon" class="h-5 w-5" />
        </button>
      </div>

      <!-- Export Controls -->
      <div class="flex space-x-2">
        <button
          v-for="format in exportFormats"
          :key="format"
          @click="$emit('export', format)"
          class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
        >
          Export as {{ format.toUpperCase() }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  ZoomInIcon,
  ZoomOutIcon,
  ArrowsPointingInIcon
} from '@heroicons/vue/24/outline'

const selectedLayout = ref('force')

const zoomControls = {
  'Zoom In': ZoomInIcon,
  'Zoom Out': ZoomOutIcon,
  'Fit': ArrowsPointingInIcon
}

const exportFormats = ['png', 'json']
</script>