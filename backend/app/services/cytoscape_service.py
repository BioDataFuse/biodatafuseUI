from pathlib import Path
from pyBiodatafuse.graph import cytoscape
from py4cytoscape import cytoscape_ping

from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.services.graph_service import GraphService
from backend.app import models


class CytoscapeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def load_graph_into_cytoscape(self, annotations: models.Annotation, graph_dir: Path, graph_name: str):
        try:
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
