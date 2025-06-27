from pathlib import Path
from pyBiodatafuse.analyzer.summarize import BioGraph
from backend.app.services.graph_service import GraphService
from backend.app import models
from sqlalchemy.ext.asyncio import AsyncSession

class AnalysisService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_graph_summary(
            self, annotation: models.Annotation, graph_dir: Path):
        try: 
            pygraph, error = GraphService.create_pygraph(annotation, graph_dir)
            if error:
                return None, f"Graph error: {error}"

            graph_obj = BioGraph(graph=pygraph)
            return graph_obj.graph_summary, None
        except Exception as e:
            return None, {"message": f"Error generating graph summary: {str(e)}"}


    async def plot_node_counts(self, annotation: models.Annotation, graph_dir: Path):
        try:
            pygraph, error = GraphService.create_pygraph(annotation, graph_dir)
            if error:
                return None, f"Graph error: {error}"

            graph_obj = BioGraph(graph=pygraph)
            fig = graph_obj.count_nodes_by_data_source(plot=True)
            return fig, None
        except Exception as e:
            return None, {"message": f"Error generating node counts: {str(e)}"}

    async def plot_edge_counts(self, annotation: models.Annotation, graph_dir: Path):
        try:
            pygraph, error = GraphService.create_pygraph(annotation, graph_dir)
            if error:
                return None, f"Graph error: {error}"

            graph_obj = BioGraph(graph=pygraph)
            fig = graph_obj.count_edge_by_data_source(plot=True)
            return fig, None
        except Exception as e:
            return None, {"message": f"Error generating edge counts: {str(e)}"}
