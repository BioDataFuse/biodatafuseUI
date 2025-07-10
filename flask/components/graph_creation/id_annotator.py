import pandas as pd
from collections import defaultdict
from pyBiodatafuse.annotators import wikipathways, disgenet, opentargets, stringdb
from pyBiodatafuse.utils import combine_sources


def process_selected_sources(
    bridgedb_df: pd.DataFrame, selected_sources_list: list, api_key: str = ""
) -> pd.DataFrame:
    """query the selected databases and convert the output to a dataframe.

    @param bridgedb_df: BridgeDb output for creating the list of gene ids to query
    @param selected_sources_list: list of selected databases
    """
    # Initialize variables
    combined_data = pd.DataFrame()
    combined_metadata = defaultdict(lambda: defaultdict(str))
    # Dictionary to map the datasource names to their corresponding functions
    data_source_functions = {
        ## TODO: "bgee": bgee.get_gene_expression,
        "disgenet": disgenet.get_gene_disease,
        ## TODO: "minerva": minera.get,
        ## TODO: "molmedb": molmedb.get_mol_gene_inhibitor,
        ## TODO: "pubchem"
        # "opentarget.gene_location": opentargets.get_gene_location,
        "opentarget.gene_ontology": opentargets.get_gene_go_process,
        "opentarget.reactome": opentargets.get_gene_reactome_pathways,
        # "opentarget.drug_interactions": opentargets.get_gene_drug_interactions,
        "opentarget.disease_associations": opentargets.get_gene_disease_associations,
        "string": stringdb.get_ppi,
        "wikipathways": wikipathways.get_gene_wikipathways
        ## TODO: "wikidata"
    }
    warnings = []  # Initialize empty list for warnings

    for source in selected_sources_list:
        if source in data_source_functions:
            if source == "disgenet":
                tmp_data, tmp_metadata = data_source_functions[source](api_key=api_key, bridgedb_df=bridgedb_df)
            else:
                tmp_data, tmp_metadata = data_source_functions[source](bridgedb_df)
            combined_metadata[source] = tmp_metadata
            if tmp_data.empty:
                warnings.append(f"No annotation available for {source}")
            if not tmp_data.empty:
                combined_data = combine_sources(bridgedb_df, [combined_data, tmp_data])

    return combined_data, combined_metadata
