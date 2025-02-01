// User Types
export interface User {
  id: number;
  email: string;
  name: string;
  api_key: string;
  is_active: boolean;
  preferences: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Identifier Types
export interface IdentifierSet {
  id: number;
  identifier_type: string;
  input_species: string;
  input_identifiers: string[];
  mapped_identifiers?: Record<string, any>;
  status: string;
  error_message?: string;
  created_at: string;
  updated_at: string;
}

export interface IdentifierProcessResponse {
  set_id: number;
  status: string;
  message: string;
  warnings?: string[];
}

// Data Source Types
export interface DataSource {
  id: string;
  name: string;
  description: string;
  requires_key: boolean;
}

export interface DataSourceRequest {
  source: string;
  api_key?: string;
}

export interface DataSourceProcessingResponse {
  status: string;
  metadata: {
    total_associations: number;
    sources_processed: string[];
    source_counts: Record<string, number>;
  };
  message: string;
}

// Network Visualization Types
export interface NodeData {
  id: string;
  type: string;
  label: string;
  properties?: Record<string, any>;
}

export interface EdgeData {
  source: string;
  target: string;
  type: string;
  weight?: number;
  properties?: Record<string, any>;
}

export interface NetworkData {
  nodes: NodeData[];
  edges: EdgeData[];
  metadata: Record<string, any>;
}

export interface VisualizationResponse {
  network_data: NetworkData;
  source_metadata: Record<string, any>;
  statistics: {
    nodes: number;
    edges: number;
    density: number;
    source_counts: Record<string, number>;
  };
}

// Visual Settings Types
export interface VisualSettings {
  layout: 'force' | 'circular' | 'concentric' | 'grid';
  nodeSize: number;
  edgeWeightThreshold: number;
  selectedSources: Record<string, boolean>;
}

export interface NodeStyle {
  color: string;
  shape: string;
  label?: string;
}

export interface EdgeStyle {
  color: string;
  width: number;
  style: string;
  label?: string;
}

export interface NetworkStyles {
  nodes: Record<string, NodeStyle>;
  edges: Record<string, EdgeStyle>;
}