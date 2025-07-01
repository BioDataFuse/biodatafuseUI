from pathlib import Path
from pyBiodatafuse.graph import cytoscape
from sqlalchemy.ext.asyncio import AsyncSession
from .graph_service import GraphService
from .. import models

class CytoscapeService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def load_graph_into_cytoscape(self, annotations: models.Annotation, graph_dir: Path, graph_name: str):
        """
        Generate graph data in Cytoscape format for client-side loading
        """
        try:
            pygraph, error = GraphService.create_pygraph(annotations, graph_dir)
            if error:
                return {"success": False, "message": error}
            
            # Use pyBiodatafuse's convert_graph_to_json function
            cytoscape_data = cytoscape.convert_graph_to_json(pygraph)
            
            return {
                "success": True, 
                "message": f"Graph data generated for '{graph_name}'",
                "graph_data": cytoscape_data
            }
            
        except Exception as e:
            return {"success": False, "message": f"Error generating graph data: {str(e)}"}