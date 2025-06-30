from pathlib import Path
from pyBiodatafuse.graph import neo4j

from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.services.graph_service import GraphService
from backend.app import models


class Neo4jService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def load_graph_into_neo4j(self, annotations: models.Annotation, graph_dir: Path):
        try:
            pygraph, error = GraphService.create_pygraph(annotations, graph_dir)
            if error:
                return {"success": False, "message": error}

            neo4j.load_graph(
                pygraph,
                uri="bolt://localhost:7687",
                username="test",
                password="password"
            )

            return {"success": True, "message": "Graph successfully loaded into Neo4j database."}
        except Exception as e:
            return {"success": False, "message": f"Error loading graph into Neo4j: {str(e)}"}
