from pathlib import Path
import pandas as pd
import networkx as nx
from typing import Optional, Tuple, Dict, Any

from pyBiodatafuse.graph import saver
from backend.app.models import Annotation


class GraphService:
    @staticmethod
    def create_pygraph(
        annotations: Annotation,
        graph_dir: Path
    ) -> Tuple[Optional[nx.MultiDiGraph], Optional[str]]:
        try:
            combined_df = pd.DataFrame(annotations.combined_df).T
            combined_metadata = annotations.combined_metadata
            opentargets_df = (
                pd.DataFrame(annotations.opentargets_df).T
                if annotations.opentargets_df else None
            )

            pygraph = saver.save_graph(
                combined_df=combined_df,
                combined_metadata=combined_metadata,
                graph_name=f"graph_{annotations.identifier_set_id}",
                disease_compound=opentargets_df,
                graph_dir=graph_dir,
            )

            if pygraph.number_of_edges() == 0:
                return None, "Graph generation succeeded, but it contains no edges."

            return pygraph, None
        except Exception as e:
            return None, str(e)
