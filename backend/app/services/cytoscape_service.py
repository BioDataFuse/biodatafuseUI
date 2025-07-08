import json
from pathlib import Path
from pyBiodatafuse.graph import cytoscape
from sqlalchemy.ext.asyncio import AsyncSession
from .graph_service import GraphService
from .. import models


class CytoscapeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cytoscape_json(self, annotations: models.Annotation, graph_dir: Path):
        try:
            pygraph, error = GraphService.create_pygraph(annotations, graph_dir)
            if error:
                return None, error

            if not pygraph.nodes() and not pygraph.edges():
                return None, "The generated graph is empty (no nodes or edges)."

            raw_graph = cytoscape.convert_graph_to_json(pygraph)
            elements_only = raw_graph.get("elements")
            cytoscape_json_data = {"elements": elements_only}

            print("Returning Cytoscape JSON:", json.dumps(cytoscape_json_data, indent=2))
            return cytoscape_json_data, None

        except Exception as e:
            return None, f"Error preparing graph data for Cytoscape: {str(e)}"

        """
        Generates Cytoscape-compatible JSON graph data.
        This function no longer interacts directly with Cytoscape or attempts to get styling from pyBiodatafuse.
        """
        try:
            # Create the NetworkX graph
            pygraph, error = GraphService.create_pygraph(annotations, graph_dir)
            if error:
                return None, error

            if not pygraph.nodes() and not pygraph.edges():
                return None, "The generated graph is empty (no nodes or edges)."

            cytoscape_json_data = cytoscape.convert_graph_to_json(pygraph)

            return cytoscape_json_data, None

        except Exception as e:
            return None, f"Error preparing graph data for Cytoscape: {str(e)}"