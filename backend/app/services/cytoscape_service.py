from pathlib import Path
from pyBiodatafuse.graph import cytoscape as cytoscape_graph
from py4cytoscape import cytoscape_ping

from sqlalchemy.ext.asyncio import AsyncSession
from .graph_service import GraphService
from .. import models
import json
import logging

logger = logging.getLogger(__name__)


class CytoscapeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def build_graph_for_cytoscape(
            self,
            set_id: int,
            annotations: models.Annotation,
            graph_dir: Path,
    ) -> models.CytoscapeFile:
        """
        Build a Cytoscape-compatible graph from annotations.
        
        Returns a CytoscapeFile object with status 'completed' or 'error'.
        """
        cytoscape = models.CytoscapeFile(
            identifier_set_id=set_id
        )
        self.db.add(cytoscape)
        await self.db.commit()

        try:
            pygraph, error = GraphService.create_pygraph(annotations, graph_dir)
            if error:
                raise ValueError(error)

            cytoscape_graph_json = cytoscape_graph.convert_graph_to_json(pygraph)
            cytoscape.cytoscape_graph = cytoscape_graph_json
            cytoscape.status = "completed"

        except ValueError as e:
            logger.warning(f"Graph creation warning for set {set_id}: {str(e)}")
            cytoscape.status = "error"
            cytoscape.error_message = str(e)
        except Exception as e:
            logger.error(f"Error building graph for set {set_id}: {str(e)}")
            cytoscape.status = "error"
            cytoscape.error_message = f"Unexpected error: {str(e)}"

        await self.db.commit()
        await self.db.refresh(cytoscape)
        return cytoscape
    
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

            cytoscape_graph.load_graph(pygraph, network_name=graph_name)
            return {"success": True, "message": f"Graph loaded into Cytoscape as '{graph_name}'."}
        except Exception as e:
            return {"success": False, "message": f"Error loading graph into Cytoscape: {str(e)}"}
        
    async def get_cytoscape_json(self, annotations: models.Annotation, graph_dir: Path):
        try:
            pygraph, error = GraphService.create_pygraph(annotations, graph_dir)
            if error:
                return None, error

            if not pygraph.nodes() and not pygraph.edges():
                return None, "The generated graph is empty (no nodes or edges)."

            raw_graph = cytoscape_graph.convert_graph_to_json(pygraph)
            elements_only = raw_graph.get("elements")
            cytoscape_json_data = {"elements": elements_only}

            return cytoscape_json_data, None

        except Exception as e:
            return None, f"Error preparing graph data for Cytoscape: {str(e)}"