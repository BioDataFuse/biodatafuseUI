import type { Core } from 'cytoscape'

export function setupNetworkEvents(cy: Core, callbacks: {
  onNodeSelect?: (node: any) => void,
  onEdgeSelect?: (edge: any) => void,
  onUnselect?: () => void,
  onViewportChange?: () => void,
  onLayoutComplete?: () => void
} = {}) {
  // Node selection
  cy.on('tap', 'node', (event) => {
    const node = event.target
    callbacks.onNodeSelect?.(node)
  })

  // Edge selection
  cy.on('tap', 'edge', (event) => {
    const edge = event.target
    callbacks.onEdgeSelect?.(edge)
  })

  // Background tap (unselect)
  cy.on('tap', (event) => {
    if (event.target === cy) {
      callbacks.onUnselect?.()
    }
  })

  // Viewport changes (zoom/pan)
  cy.on('viewport', () => {
    callbacks.onViewportChange?.()
  })

  // Layout completion
  cy.on('layoutstop', () => {
    callbacks.onLayoutComplete?.()
  })

  // Double-click to zoom
  cy.on('dbltap', 'node', (event) => {
    event.preventDefault()
    const node = event.target
    cy.animate({
      zoom: 2,
      center: {
        eles: node
      },
      duration: 500
    })
  })

  // Hover effects
  cy.on('mouseover', 'node', (event) => {
    const node = event.target
    node.addClass('hover')
    node.neighborhood().addClass('hover')
  })

  cy.on('mouseout', 'node', (event) => {
    const node = event.target
    node.removeClass('hover')
    node.neighborhood().removeClass('hover')
  })

  // Edge hover effects
  cy.on('mouseover', 'edge', (event) => {
    const edge = event.target
    edge.addClass('hover')
    edge.connectedNodes().addClass('hover')
  })

  cy.on('mouseout', 'edge', (event) => {
    const edge = event.target
    edge.removeClass('hover')
    edge.connectedNodes().removeClass('hover')
  })

  return {
    destroy: () => {
      cy.removeAllListeners()
    }
  }
}