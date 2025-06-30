import type { Core } from 'cytoscape'

export class NetworkAnalysis {
  private cy: Core

  constructor(cy: Core) {
    this.cy = cy
  }

  public getStatistics() {
    const nodes = this.cy.nodes(':visible')
    const edges = this.cy.edges(':visible')
    const nodeCount = nodes.length
    const edgeCount = edges.length

    return {
      nodes: nodeCount,
      edges: edgeCount,
      density: this.calculateDensity(nodeCount, edgeCount),
      avgDegree: this.calculateAverageDegree(nodeCount, edgeCount),
      clusters: this.detectClusters().length,
      nodeTypes: this.getNodeTypeCounts(),
      edgeTypes: this.getEdgeTypeCounts()
    }
  }

  private calculateDensity(nodeCount: number, edgeCount: number): number {
    if (nodeCount <= 1) return 0
    const maxEdges = (nodeCount * (nodeCount - 1)) / 2
    return edgeCount / maxEdges
  }

  private calculateAverageDegree(nodeCount: number, edgeCount: number): number {
    if (nodeCount === 0) return 0
    return (2 * edgeCount) / nodeCount
  }

  public detectClusters(): any[] {
    // Implement community detection algorithm
    // This is a simple example using connected components
    const clusters: Set<any>[] = []
    const visited = new Set()

    this.cy.nodes().forEach(node => {
      if (!visited.has(node.id())) {
        const cluster = this.getBFS(node, visited)
        if (cluster.size > 0) {
          clusters.push(cluster)
        }
      }
    })

    return clusters
  }

  private getBFS(startNode: any, visited: Set<string>): Set<string> {
    const cluster = new Set<string>()
    const queue = [startNode]
    
    while (queue.length > 0) {
      const node = queue.shift()
      if (!visited.has(node.id())) {
        visited.add(node.id())
        cluster.add(node.id())
        
        node.neighborhood('node').forEach(neighbor => {
          if (!visited.has(neighbor.id())) {
            queue.push(neighbor)
          }
        })
      }
    }

    return cluster
  }

  public getNodeTypeCounts(): Record<string, number> {
    const counts: Record<string, number> = {}
    this.cy.nodes().forEach(node => {
      const type = node.data('type')
      counts[type] = (counts[type] || 0) + 1
    })
    return counts
  }

  public getEdgeTypeCounts(): Record<string, number> {
    const counts: Record<string, number> = {}
    this.cy.edges().forEach(edge => {
      const type = edge.data('type')
      counts[type] = (counts[type] || 0) + 1
    })
    return counts
  }

  public findShortestPath(source: string, target: string) {
    const dijkstra = this.cy.elements().dijkstra({
      root: `#${source}`,
      directed: false
    })
    return dijkstra.pathTo(this.cy.$(`#${target}`))
  }

  public findCentralNodes(count = 5) {
    const centrality = this.cy.nodes().betweennessCentrality()
    return this.cy.nodes()
      .sort((a, b) => centrality.betweenness(b) - centrality.betweenness(a))
      .slice(0, count)
  }

  public getNodeNeighborhood(nodeId: string, depth = 1) {
    const node = this.cy.$id(nodeId)
    if (!node.length) return null

    let neighborhood = node
    for (let i = 0; i < depth; i++) {
      neighborhood = neighborhood.add(neighborhood.neighborhood())
    }
    return neighborhood
  }
}