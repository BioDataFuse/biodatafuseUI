export { default as NetworkToolbar } from './NetworkToolbar.vue'
export { default as NetworkStats } from './NetworkStats.vue'
export { default as NetworkFilters } from './NetworkFilters.vue'
export { default as ElementDetails } from './ElementDetails.vue'

// Types
export interface NetworkElement {
  type: 'node' | 'edge'
  data: Record<string, any>
}

export interface NetworkSettings {
  layout: 'force' | 'circular' | 'concentric' | 'grid'
  filters: {
    sources: Record<string, boolean>
    nodeTypes: Record<string, boolean>
    edgeWeight: number
  }
}

export interface NetworkStats {
  nodes: number
  edges: number
  density: number
  avgDegree: number
  clusters: number
}