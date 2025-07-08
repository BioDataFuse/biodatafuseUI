from pathlib import Path
from pyBiodatafuse.graph import cytoscape as cytoscape_graph
from py4cytoscape import cytoscape_ping

from fastapi import Depends, HTTPException
from ..database import get_db
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .graph_service import GraphService
from .. import models

class CytoscapeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def build_graph_for_cytoscape(
            self,
            set_id: int,
            annotations: models.Annotation,
            graph_dir: Path,
    ) -> models.CytoscapeFile:
        
        cytoscape = models.CytoscapeFile(
            identifier_set_id=set_id
        )
        self.db.add(cytoscape)
        await self.db.commit()

        pygraph, error = GraphService.create_pygraph(annotations, graph_dir)
        if error:
                return None, f"Graph error: {error}"

        cytoscape_graph_json = cytoscape_graph.convert_graph_to_json(pygraph)
        cytoscape.cytoscape_graph = cytoscape_graph_json
        cytoscape.status = "completed"

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
        