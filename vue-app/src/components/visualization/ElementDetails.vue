<template>
  <div class="bg-white shadow rounded-md p-4">
    <div class="flex justify-between items-start">
      <h3 class="text-lg font-medium text-gray-900">
        {{ element.type === 'node' ? 'Node Details' : 'Edge Details' }}
      </h3>
      <button
        @click="$emit('close')"
        class="text-gray-400 hover:text-gray-500"
      >
        <XMarkIcon class="h-5 w-5" />
      </button>
    </div>

    <div class="mt-4">
      <!-- Type Badge -->
      <div class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
           :class="typeBadgeClasses">
        {{ element.data.type }}
      </div>

      <!-- Properties -->
      <dl class="mt-4 grid grid-cols-2 gap-4">
        <template v-for="(value, key) in displayProperties" :key="key">
          <div class="col-span-1">
            <dt class="text-sm font-medium text-gray-500">{{ formatKey(key) }}</dt>
            <dd class="mt-1 text-sm text-gray-900">
              <template v-if="isLink(value)">
                <a :href="value" target="_blank" class="text-indigo-600 hover:text-indigo-900">
                  {{ formatValue(value) }}
                  <ExternalLinkIcon class="inline h-4 w-4 ml-1" />
                </a>
              </template>
              <template v-else>
                {{ formatValue(value) }}
              </template>
            </dd>
          </div>
        </template>
      </dl>

      <!-- Actions -->
      <div class="mt-6 flex space-x-3">
        <button
          v-if="element.type === 'node'"
          @click="$emit('highlight-neighbors')"
          class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          Highlight Neighbors
        </button>
        <button
          @click="$emit('center-element')"
          class="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
        >
          Center View
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { XMarkIcon, ExternalLinkIcon } from '@heroicons/vue/24/outline'

const props = defineProps<{
  element: {
    type: 'node' | 'edge'
    data: Record<string, any>
  }
}>()

// Computed properties
const displayProperties = computed(() => {
  const { id, type, ...rest } = props.element.data
  return rest
})

const typeBadgeClasses = computed(() => {
  const baseClasses = 'bg-opacity-10'
  switch (props.element.data.type) {
    case 'Gene':
      return `${baseClasses} bg-blue-100 text-blue-800`
    case 'Disease':
      return `${baseClasses} bg-red-100 text-red-800`
    case 'Protein':
      return `${baseClasses} bg-green-100 text-green-800`
    case 'Pathway':
      return `${baseClasses} bg-purple-100 text-purple-800`
    default:
      return `${baseClasses} bg-gray-100 text-gray-800`
  }
})

// Helper functions
function formatKey(key: string): string {
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function formatValue(value: any): string {
  if (value === null || value === undefined) return '-'
  if (typeof value === 'boolean') return value ? 'Yes' : 'No'
  if (typeof value === 'number') {
    return value < 1 ? value.toFixed(3) : value.toLocaleString()
  }
  if (Array.isArray(value)) return value.join(', ')
  return String(value)
}

function isLink(value: any): boolean {
  if (typeof value !== 'string') return false
  return value.startsWith('http://') || value.startsWith('https://')
}
</script>