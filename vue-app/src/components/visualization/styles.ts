export const nodeColors = {
  Gene: '#4299E1',     // blue-500
  Disease: '#F56565',  // red-500
  Protein: '#48BB78',  // green-500
  Pathway: '#9F7AEA',  // purple-500
  Compound: '#ED8936',  // orange-500
  Default: '#A0AEC0'   // gray-500
}

export const edgeColors = {
  'Disease Association': '#FC8181',     // red-400
  'Protein Interaction': '#68D391',     // green-400
  'Pathway Member': '#B794F4',          // purple-400
  'Compound Interaction': '#F6AD55',    // orange-400
  'Default': '#CBD5E0'                  // gray-400
}

export const generateNetworkStyle = () => [
  {
    selector: 'node',
    style: {
      'background-color': 'data(color)',
      'label': 'data(label)',
      'color': '#2D3748',           // gray-800
      'text-outline-color': '#fff',
      'text-outline-width': '2px',
      'font-size': '12px',
      'text-valign': 'center',
      'text-halign': 'center',
      'text-max-width': '100px',
      'text-wrap': 'ellipsis',
      'min-zoomed-font-size': '8px',
      'transition-property': 'background-color, border-color, border-width',
      'transition-duration': '0.2s'
    }
  },
  {
    selector: 'edge',
    style: {
      'width': 'data(weight)',
      'line-color': 'data(color)',
      'target-arrow-color': 'data(color)',
      'target-arrow-shape': 'triangle',
      'curve-style': 'bezier',
      'opacity': 0.7,
      'transition-property': 'line-color, target-arrow-color, opacity, width',
      'transition-duration': '0.2s'
    }
  },
  {
    selector: '.highlighted',
    style: {
      'background-color': '#FAF089',  // yellow-300
      'border-width': '3px',
      'border-color': '#D69E2E',      // yellow-600
      'border-opacity': 0.8,
      'z-index': 999
    }
  },
  {
    selector: '.highlighted-edge',
    style: {
      'width': 4,
      'line-color': '#D69E2E',        // yellow-600
      'target-arrow-color': '#D69E2E', // yellow-600
      'opacity': 1,
      'z-index': 999
    }
  },
  {
    selector: '.faded',
    style: {
      'opacity': 0.2
    }
  },
  {
    selector: '.hidden',
    style: {
      'display': 'none'
    }
  }
]

export const layouts = {
  force: {
    name: 'fcose',
    quality: 'default',
    animate: true,
    animationDuration: 1000,
    randomize: true,
    nodeRepulsion: 5000,
    idealEdgeLength: 100,
    edgeElasticity: 0.45,
    numIter: 2500,
    padding: 30
  },
  circular: {
    name: 'circle',
    animate: true,
    animationDuration: 1000,
    radius: undefined,
    startAngle: 3/2 * Math.PI,
    clockwise: true,
    padding: 30
  },
  concentric: {
    name: 'concentric',
    animate: true,
    animationDuration: 1000,
    minNodeSpacing: 50,
    concentric: (node: any) => node.degree(),
    levelWidth: () => 1,
    padding: 30
  },
  grid: {
    name: 'grid',
    animate: true,
    animationDuration: 1000,
    padding: 30,
    avoidOverlap: true,
    nodeDimensionsIncludeLabels: true
  }
}

export const visualizationDefaults = {
  nodeSize: 30,
  edgeWeightThreshold: 0.3,
  minZoom: 0.1,
  maxZoom: 3,
  wheelSensitivity: 0.1,
  animation: {
    duration: 300,
    easing: 'ease-in-out'
  }
}