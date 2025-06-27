# backend/app/services/graph_analysis_service.py

from pyBiodatafuse.viz.patent_data import get_patent_data, _process_data_for_plot
from pyBiodatafuse import id_mapper

class GraphAnalysisService:
    def __init__(self):
        pass

    async def run_patent_analysis(self, chem_list):
        # 1. Map compound names to PubChem CIDs
        pubchem_df, _ = id_mapper.pubchem_xref(
            identifiers=chem_list,
            indentifier_type="name"
        )

        # 2. Fetch patent metadata
        metadata_df = get_patent_data(pubchem_df)

        # 3. Format for plotting
        processed_df = _process_data_for_plot(metadata_df)

        return processed_df
