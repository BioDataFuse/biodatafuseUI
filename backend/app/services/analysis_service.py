from pathlib import Path
from pyBiodatafuse.analyzer.summarize import BioGraph
from backend.app.services.graph_service import GraphService
from backend.app import models
from sqlalchemy.ext.asyncio import AsyncSession
import matplotlib.pyplot as plt
import pandas as pd

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
            summary_html = graph_obj.graph_summary
            return {"summary_html": summary_html}, None

        except Exception as e:
            return None, {"message": f"Error generating graph summary: {str(e)}"}


    async def plot_node_counts(self, annotation: models.Annotation, graph_dir: Path):
        try:
            pygraph, error = GraphService.create_pygraph(annotation, graph_dir)
            if error:
                return None, f"Graph error: {error}"

            graph_obj = BioGraph(graph=pygraph)
            data = graph_obj.count_nodes_by_data_source(plot=False)

            # Aggregate counts
            grouped = data.groupby(['node_type', 'node_source'])['count'].sum().unstack().fillna(0)

            # Create bar plot with matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))
            grouped.plot(kind='bar', stacked=True, ax=ax)

            ax.set_title("Node Count by Source")
            ax.set_xlabel("Node Type")
            ax.set_ylabel("Count")
            ax.legend(title="Source", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()

            return fig, None

        except Exception as e:
            return None, {"message": f"Error generating node counts: {str(e)}"}


    async def plot_edge_counts(self, annotation: models.Annotation, graph_dir: Path):
        try:
            pygraph, error = GraphService.create_pygraph(annotation, graph_dir)
            if error:
                return None, f"Graph error: {error}"

            graph_obj = BioGraph(graph=pygraph)
            data = graph_obj.count_edge_by_data_source(plot=False)

            # Aggregate and pivot to get grouped bar chart
            grouped = data.groupby(['edge_type', 'edge_source'])['count'].sum().unstack().fillna(0)

            # Plot using matplotlib
            fig, ax = plt.subplots(figsize=(10, 6))
            grouped.plot(kind='bar', stacked=True, ax=ax)

            ax.set_title("Edge Count by Source")
            ax.set_xlabel("Edge Type")
            ax.set_ylabel("Count")
            ax.legend(title="Source", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()

            return fig, None

        except Exception as e:
            return None, {"message": f"Error generating edge counts: {str(e)}"}