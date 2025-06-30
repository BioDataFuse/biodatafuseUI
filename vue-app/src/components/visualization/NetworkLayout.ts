import { layouts } from './styles'
import type { Core, NodeSingular } from 'cytoscape'

export class NetworkLayout {
  private cy: Core
  private currentLayout: any
  private options: any

  constructor(cy: Core, initialLayout = 'force') {
    this.cy = cy
    this.options = { ...layouts[initialLayout] }
    this.currentLayout = null
  }

  public run(layoutName: string = 'force', options = {}) {
    // Stop any running layout
    if (this.currentLayout?.stop) {
      this.currentLayout.stop()
    }

    // Get base layout options
    const baseOptions = layouts[layoutName] || layouts.force

    // Create new layout
    this.currentLayout = this.cy.layout({
      ...baseOptions,
      ...options,
      // Add additional handlers
      fit: true,
      stop: () => {
        this.cy.nodes().unlock()
        // Emit layout complete event if needed
      }
    })

    // Run the layout
    this.currentLayout.run()
  }

  public updateNodePositions(nodes: NodeSingular[], animate = true) {
    const duration = animate ? 500 : 0
    nodes.forEach(node => {
      const position = this.calculateOptimalPosition(node)
      node.animate({
        position,
        duration,
        easing: 'ease-in-out'
      })
    })
  }

  private calculateOptimalPosition(node: NodeSingular) {
    // Implement position calculation based on node type and connections
    const neighbors = node.neighborhood()
    const centerX = this.cy.width() / 2
    const centerY = this.cy.height() / 2
    
    if (neighbors.length === 0) {
      return { x: centerX, y: centerY }
    }

    // Calculate average position of neighbors
    const positions = neighbors.nodes().map(n => n.position())
    const avgX = positions.reduce((sum, pos) => sum + pos.x, 0) / positions.length
    const avgY = positions.reduce((sum, pos) => sum + pos.y, 0) / positions.length

    return { x: avgX, y: avgY }
  }

  public focusOnElement(element: any, zoom = 1.5) {
    this.cy.animate({
      center: {
        eles: element
      },
      zoom: zoom,
      duration: 500
    })
  }

  public resetView() {
    this.cy.animate({
      fit: {
        padding: 50
      },
      duration: 500
    })
  }

  public highlightNeighborhood(node: NodeSingular) {
    // Reset previous highlights
    this.cy.elements().removeClass('highlighted highlighted-edge faded')

    // Get neighborhood
    const neighborhood = node.neighborhood().add(node)
    
    // Highlight node and its neighborhood
    node.addClass('highlighted')
    neighborhood.edges().addClass('highlighted-edge')
    
    // Fade out everything else
    this.cy.elements().not(neighborhood).addClass('faded')
  }

  public clearHighlights() {
    this.cy.elements().removeClass('highlighted highlighted-edge faded')
  }

  public filterByType(types: string[]) {
    this.cy.nodes().forEach(node => {
      const type = node.data('type')
      if (types.includes(type)) {
        node.removeClass('hidden')
      } else {
        node.addClass('hidden')
      }
    })
  }

  public filterEdgesByWeight(threshold: number) {
    this.cy.edges().forEach(edge => {
      const weight = edge.data('weight') || 0
      if (weight >= threshold) {
        edge.removeClass('hidden')
      } else {
        edge.addClass('hidden')
      }
    })
  }

  public destroy() {
    if (this.currentLayout?.stop) {
      this.currentLayout.stop()
    }
  }
}