import { nodeColors, edgeColors } from './styles'

export function addDisGeNETElements(
  item: any,
  nodes: Map<string, any>,
  edges: any[]
) {
  // Add gene node
  if (!nodes.has(item.gene_id)) {
    nodes.set(item.gene_id, {
      group: 'nodes',
      data: {
        id: item.gene_id,
        label: item.gene_symbol || item.gene_id,
        type: 'Gene',
        color: nodeColors.Gene,
        source: 'DisGeNET',
        ...item
      }
    })
  }

  // Add disease node
  if (!nodes.has(item.disease_id)) {
    nodes.set(item.disease_id, {
      group: 'nodes',
      data: {
        id: item.disease_id,
        label: item.disease_name || item.disease_id,
        type: 'Disease',
        color: nodeColors.Disease,
        source: 'DisGeNET',
        ...item
      }
    })
  }

  // Add edge
  const edgeId = `disGeNET-${item.gene_id}-${item.disease_id}`
  edges.push({
    group: 'edges',
    data: {
      id: edgeId,
      source: item.gene_id,
      target: item.disease_id,
      type: 'Disease Association',
      color: edgeColors['Disease Association'],
      weight: normalizeScore(item.score, 'DisGeNET'),
      score: item.score,
      evidence: item.evidence_count,
      source_db: 'DisGeNET',
      sourceType: 'Disease Association',
      ...item
    }
  })
}

export function addSTRINGElements(
  item: any,
  nodes: Map<string, any>,
  edges: any[]
) {
  // Add protein nodes
  if (!nodes.has(item.protein_a)) {
    nodes.set(item.protein_a, {
      group: 'nodes',
      data: {
        id: item.protein_a,
        label: item.protein_a_symbol || item.protein_a,
        type: 'Protein',
        color: nodeColors.Protein,
        source: 'STRING',
        ...item
      }
    })
  }

  if (!nodes.has(item.protein_b)) {
    nodes.set(item.protein_b, {
      group: 'nodes',
      data: {
        id: item.protein_b,
        label: item.protein_b_symbol || item.protein_b,
        type: 'Protein',
        color: nodeColors.Protein,
        source: 'STRING',
        ...item
      }
    })
  }

  // Add edge
  const edgeId = `string-${item.protein_a}-${item.protein_b}`
  edges.push({
    group: 'edges',
    data: {
      id: edgeId,
      source: item.protein_a,
      target: item.protein_b,
      type: 'Protein Interaction',
      color: edgeColors['Protein Interaction'],
      weight: normalizeScore(item.combined_score, 'STRING'),
      score: item.combined_score,
      interaction_types: item.interaction_types,
      source_db: 'STRING',
      sourceType: 'Protein Interaction',
      ...item
    }
  })
}

export function addKEGGElements(
  item: any,
  nodes: Map<string, any>,
  edges: any[]
) {
  // Add gene/protein node
  if (!nodes.has(item.gene_id)) {
    nodes.set(item.gene_id, {
      group: 'nodes',
      data: {
        id: item.gene_id,
        label: item.gene_symbol || item.gene_id,
        type: 'Gene',
        color: nodeColors.Gene,
        source: 'KEGG',
        ...item
      }
    })
  }

  // Add pathway node
  if (!nodes.has(item.pathway_id)) {
    nodes.set(item.pathway_id, {
      group: 'nodes',
      data: {
        id: item.pathway_id,
        label: item.pathway_name || item.pathway_id,
        type: 'Pathway',
        color: nodeColors.Pathway,
        source: 'KEGG',
        pathway_class: item.pathway_class,
        ...item
      }
    })
  }

  // Add edge
  const edgeId = `kegg-${item.gene_id}-${item.pathway_id}`
  edges.push({
    group: 'edges',
    data: {
      id: edgeId,
      source: item.gene_id,
      target: item.pathway_id,
      type: 'Pathway Member',
      color: edgeColors['Pathway Member'],
      weight: 1, // KEGG doesn't provide edge weights
      source_db: 'KEGG',
      sourceType: 'Pathway Membership',
      ...item
    }
  })
}

// Helper functions for data transformation
function normalizeScore(score: number, source: string): number {
  switch (source) {
    case 'DisGeNET':
      // DisGeNET scores are between 0 and 1
      return score
    case 'STRING':
      // STRING scores are between 0 and 1000
      return score / 1000
    default:
      return score
  }
}

export interface NetworkData {
  nodes: Map<string, any>
  edges: any[]
}

export function transformNetworkData(data: any[]): NetworkData {
  const nodes = new Map()
  const edges: any[] = []

  data.forEach(item => {
    switch (item.source) {
      case 'DisGeNET':
        addDisGeNETElements(item, nodes, edges)
        break
      case 'STRING':
        addSTRINGElements(item, nodes, edges)
        break
      case 'KEGG':
        addKEGGElements(item, nodes, edges)
        break
    }
  })

  return { nodes, edges }
}

export function mergeNetworkData(datasets: NetworkData[]): NetworkData {
  const mergedNodes = new Map()
  const mergedEdges: any[] = []
  const processedEdges = new Set()

  datasets.forEach(dataset => {
    // Merge nodes
    dataset.nodes.forEach((node, id) => {
      if (!mergedNodes.has(id)) {
        mergedNodes.set(id, node)
      } else {
        // Merge node properties if node already exists
        const existingNode = mergedNodes.get(id)
        mergedNodes.set(id, {
          ...existingNode,
          data: {
            ...existingNode.data,
            ...node.data,
            sources: [...(existingNode.data.sources || []), node.data.source]
          }
        })
      }
    })

    // Merge edges
    dataset.edges.forEach(edge => {
      const edgeKey = `${edge.data.source}-${edge.data.target}-${edge.data.type}`
      if (!processedEdges.has(edgeKey)) {
        mergedEdges.push(edge)
        processedEdges.add(edgeKey)
      }
    })
  })

  return { nodes: mergedNodes, edges: mergedEdges }
}

export function getNetworkStatistics(networkData: NetworkData) {
  const nodeCount = networkData.nodes.size
  const edgeCount = networkData.edges.length

  return {
    nodes: nodeCount,
    edges: edgeCount,
    density: calculateNetworkDensity(nodeCount, edgeCount),
    nodeTypes: countNodeTypes(networkData.nodes),
    edgeTypes: countEdgeTypes(networkData.edges)
  }
}

function calculateNetworkDensity(nodes: number, edges: number): number {
  if (nodes <= 1) return 0
  const maxPossibleEdges = (nodes * (nodes - 1)) / 2
  return edges / maxPossibleEdges
}

function countNodeTypes(nodes: Map<string, any>): Record<string, number> {
  const counts: Record<string, number> = {}
  nodes.forEach(node => {
    const type = node.data.type
    counts[type] = (counts[type] || 0) + 1
  })
  return counts
}

function countEdgeTypes(edges: any[]): Record<string, number> {
  return edges.reduce((counts: Record<string, number>, edge) => {
    const type = edge.data.type
    counts[type] = (counts[type] || 0) + 1
    return counts
  }, {})
}