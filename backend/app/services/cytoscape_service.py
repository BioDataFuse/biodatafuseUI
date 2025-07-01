from pathlib import Path
from pyBiodatafuse.graph import cytoscape
import networkx as nx
from sqlalchemy.ext.asyncio import AsyncSession
from .graph_service import GraphService
from .. import models

class CytoscapeService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def generate_graph_data(self, annotations: models.Annotation, graph_dir: Path, graph_name: str):
        """
        Generate graph data in Cytoscape.js format for client-side loading
        """
        try:
            pygraph, error = GraphService.create_pygraph(annotations, graph_dir)
            if error:
                return {"success": False, "message": error}
            
            # Convert NetworkX graph to Cytoscape.js format
            cytoscape_data = self._networkx_to_cytoscape_js(pygraph)
            
            return {
                "success": True, 
                "message": f"Graph data generated for '{graph_name}'",
                "graph_data": cytoscape_data
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error generating graph data: {str(e)}"}
    
    def _networkx_to_cytoscape_js(self, graph):
        """
        Convert NetworkX graph to Cytoscape.js format using pyBiodatafuse
        """
        # Use the existing convert_graph_to_json function from pyBiodatafuse
        return cytoscape.convert_graph_to_json(graph)

    # Keep the original method for local development
    async def load_graph_into_cytoscape_local(self, annotations: models.Annotation, graph_dir: Path, graph_name: str):
        """
        Original method - only use for local development
        """
        try:
            from py4cytoscape import cytoscape_ping
            
            if cytoscape_ping() != "You are connected to Cytoscape!":
                return {
                    "success": False,
                    "message": "Cytoscape is not running or REST API is unreachable. Please ensure Cytoscape desktop is open."
                }
            pygraph, error = GraphService.create_pygraph(annotations, graph_dir)
            if error:
                return {"success": False, "message": error}
            cytoscape.load_graph(pygraph, network_name=graph_name)
            return {"success": True, "message": f"Graph loaded into Cytoscape as '{graph_name}'."}
        except Exception as e:
            return {"success": False, "message": f"Error loading graph into Cytoscape: {str(e)}"}