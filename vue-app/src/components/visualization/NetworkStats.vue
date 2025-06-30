<template>
  <div class="bg-white shadow rounded-md p-4">
    <h3 class="text-lg font-medium text-gray-900 mb-4">Network Statistics</h3>
    <dl class="grid grid-cols-2 gap-4">
      <div v-for="(value, key) in stats" :key="key" class="col-span-1">
        <dt class="text-sm font-medium text-gray-500">{{ formatKey(key) }}</dt>
        <dd class="mt-1 text-2xl font-semibold text-gray-900">{{ formatValue(value) }}</dd>
      </div>
    </dl>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  stats: Record<string, number>
}>()

function formatKey(key: string): string {
  return key
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

function formatValue(value: number): string {
  if (value < 1) {
    return value.toFixed(3)
  }
  return value.toLocaleString()
}
</script>