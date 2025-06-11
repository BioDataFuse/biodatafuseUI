import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import warnings

import aiohttp
import pandas as pd
from pyBiodatafuse.annotators import (
    bgee,
    disgenet,
    minerva,
    molmedb,
    opentargets,
    pubchem,
    stringdb,
    wikipathways,
)
from pyBiodatafuse.utils import (
    combine_sources,
    create_harmonized_input_file,
    create_or_append_to_metadata,
)
import pyBiodatafuse.constants as constants
from pyBiodatafuse.graph import generator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models


class DataSourceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.available_sources = {
            "bgee": {
                "name": constants.BGEE,
                "description": "Gene expression levels in different tissues",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.BGEE_ENDPOINT,
            },
            "disgenet": {
                "name": constants.DISGENET,
                "description": "Gene-disease associations",
                "requires_key": True,
                "requires_map_name": False,
                "base_url": constants.DISGENET_ENDPOINT,
            },
            "wikipathways_pathways": {
                "name": f"{constants.WIKIPATHWAYS} - Pathways",
                "description": "Biological pathway",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.WIKIPATHWAYS_ENDPOINT,
            },
            "wikipathways_interactions": {
                "name": f"{constants.WIKIPATHWAYS} - Pathways and molecular interactions",
                "description": "Biological pathway",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.WIKIPATHWAYS_ENDPOINT,
            },
            "kegg": {
                "name": constants.KEGG,
                "description": "Kyoto Encyclopedia of Genes and Genomes",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.KEGG_ENDPOINT,
            },
            "minerva": {
                "name": constants.MINERVA,
                "description": "System biology networks",
                "requires_key": False,
                "requires_map_name": True,
                "base_url": constants.MINERVA_ENDPOINT,
            },
            "stringdb": {
                "name": constants.STRING,
                "description": "Protein-protein interaction network",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.STRING_ENDPOINT,
            },
            "opentargets_go": {
                "name": f"{constants.OPENTARGETS} - Gene Ontology (GO)",
                "description": "Target discovery and prioritization",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.OPENTARGETS_ENDPOINT,
            },
            "opentargets_reactome": {
                "name": f"{constants.OPENTARGETS} - Reactome pathways",
                "description": "Target discovery and prioritization",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.OPENTARGETS_ENDPOINT,
            },
            "opentargets_disease_compound": {
                "name": f"{constants.OPENTARGETS} - Disease to compound annotation",
                "description": "Target discovery and prioritization",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.OPENTARGETS_ENDPOINT,
            },
            "opentargets_gene_compound": {
                "name": f"{constants.OPENTARGETS} - Gene to compound annotation",
                "description": "Target discovery and prioritization",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.OPENTARGETS_ENDPOINT,
            },
            "pubchem_assays": {
                "name": f"{constants.PUBCHEM} - Assays",
                "description": "Chemical information",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.PUBCHEM_ENDPOINT,
            },
            "molmedb_compounds": {
                "name": f"{constants.MOLMEDB} - Transporter inhibitor annotation",
                "description": "molecules' interactions with membranes",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.MOLMEDB_ENDPOINT,
            },
        }

    async def get_available_sources(self) -> List[Dict]:
        """Get list of available data sources"""
        return [{"id": key, **value} for key, value in self.available_sources.items()]

    async def process_selected_sources(
        self,
        set_id: int,
        datasources: List[Dict],  # List of {source: str, api_key: Optional[str], map_name: Optional[str]}
    ) -> Tuple[pd.DataFrame, Dict, str, pd.DataFrame]:

        """Process selected data sources with their API keys"""
        identifier_set = await self.db.execute(
            select(models.IdentifierSet).where(models.IdentifierSet.id == set_id)
        )
        identifier_set = identifier_set.scalar_one_or_none()

        if not identifier_set:
            raise ValueError("Identifier set not found")

        try:
            # bridgedb_json = json.loads(identifier_set.mapped_identifiers_subset)
            # bridgedb_df = pd.DataFrame(bridgedb_json)
            bridgedb_df = pd.DataFrame(identifier_set.mapped_identifiers).T
            bridgedb_df = bridgedb_df.rename(columns={'identifier_source': 'identifier.source', 'target_source': 'target.source'})
            bridgedb_metadata = identifier_set.bridgedb_metadata

        except Exception as e:
            raise ValueError (f"Error loading mapped_identifiers_subset: {e}")
        
        dataframes = []
        metadata = []
        opentargets_df = None
        # metadata = {"sources_processed": [], "source_counts": {}, "warnings": []}
        
        try:
            # Capture any warnings generated by the pyBiodatafuse package function call
            with warnings.catch_warnings(record=True) as caught_warnings:
                warnings.simplefilter("always")

                # Process each selected data source
                for source_info in datasources:
                    source_name = source_info["source"]
                    api_key = source_info.get("api_key")
                    map_name = source_info.get("map_name")
                    try:
                        if source_name == "disgenet":

                            disgenet_df, disgenet_metadata =disgenet.get_gene_disease(
                                api_key=api_key, bridgedb_df=bridgedb_df
                            )
                            dataframes.append(disgenet_df)
                            metadata.append(disgenet_metadata)
                        elif source_name == "opentargets_disease_compound":
                            disease_mapping_df = create_harmonized_input_file(disgenet_df, constants.DISGENET_DISEASE_COL, "EFO", "UMLS")
                            opentargets_df, opentargets_metadata = opentargets.get_disease_compound_interactions(
                                disease_mapping_df
                            )
                            metadata.append(opentargets_metadata)
                        elif source_name == "bgee":
                            bgee_df, bgee_metadata = bgee.get_gene_expression(
                                bridgedb_df=bridgedb_df
                            )
                            dataframes.append(bgee_df)
                            metadata.append(bgee_metadata)
                        elif source_name == "minerva":
                            minerva_df, minerva_metadata = minerva.get_gene_minerva_pathways(
                                bridgedb_df=bridgedb_df, map_name=map_name
                            )
                            dataframes.append(minerva_df)
                            metadata.append(minerva_metadata)
                        elif source_name == "wikipathways_pathways":
                            wikipathways_df, wikipathways_metadata = wikipathways.get_gene_wikipathways(
                                bridgedb_df=bridgedb_df
                            )
                            dataframes.append(wikipathways_df)
                            metadata.append(wikipathways_metadata)
                        elif source_name == "wikipathways_interactions":
                            wikipathways_mol_df, wikipathways_mol_metadata = wikipathways.get_gene_wikipathways(
                                bridgedb_df=bridgedb_df, query_interactions=True
                            )
                            dataframes.append(wikipathways_mol_df)
                            metadata.append(wikipathways_mol_metadata)
                        elif source_name == "opentargets_reactome":
                            opentargets_reactome_df, opentargets_reactome_metadata = opentargets.get_gene_reactome_pathways(
                                bridgedb_df=bridgedb_df
                            ) 
                            dataframes.append(opentargets_reactome_df)
                            metadata.append(opentargets_reactome_metadata)
                        # elif source_name == "kegg":
                        #     kegg_df, kegg_metadata = bgee.get_kegg_data(
                        #         bridgedb_df=bridgedb_df
                        #     ) #TODO: implement kegg data retrieval
                        #     dataframes.append(kegg_df)
                        #     metadata.append(kegg_metadata)
                        elif source_name == "opentargets_go":
                            opentargets_go_df, opentargets_go_metadata = opentargets.get_gene_go_process(
                                bridgedb_df=bridgedb_df
                            )
                            dataframes.append(opentargets_go_df)
                            metadata.append(opentargets_go_metadata)
                        elif source_name == "opentargets_gene_compound":
                            opentargets_compound_df, opentargets_compound_metadata = opentargets.get_gene_compound_interactions(
                                bridgedb_df=bridgedb_df
                            )
                            dataframes.append(opentargets_compound_df)
                            metadata.append(opentargets_compound_metadata)
                        elif source_name == "pubchem_assays":
                            pubchem_assay_df, pubchem_assay_metadata = pubchem.get_protein_compound_screened(
                                bridgedb_df=bridgedb_df
                            )
                            dataframes.append(pubchem_assay_df)
                            metadata.append(pubchem_assay_metadata)
                        elif source_name == "molmedb_compounds":
                            inhibitor_df, inhibitor_metadata = molmedb.get_gene_compound_inhibitor(bridgedb_df=bridgedb_df)
                            print(f"Retrieved Inhibitor DataFrame: {inhibitor_df.head()}")  #TODO: check why the PPI dataframe is empty
                            dataframes.append(inhibitor_df)
                            metadata.append(inhibitor_metadata)
                        elif source_name == "stringdb":
                            ppi_df, ppi_metadata = stringdb.get_ppi(bridgedb_df=bridgedb_df)
                            print(f"Retrieved PPI DataFrame: {ppi_df.head()}") #TODO: check why the PPI dataframe is empty
                            dataframes.append(ppi_df)
                            metadata.append(ppi_metadata)

                        else:
                            continue



                        # metadata["sources_processed"].append(source_name)
                        # metadata["source_counts"][source_name] = source_metadata["count"]
                        # if not df.empty:
                        #     dataframes.append(df)
                        # else:
                        #     metadata["warnings"].append(f"No data found for {source_name}")

                    except Exception as e:
                        f"Error processing {source_name}: {str(e)}"
                        
                        continue

            warning_messages = [str(w.message) for w in caught_warnings]
            if warning_messages:
                print(f"Warnings captured: {warning_messages}")

            # Combine all dataframes
            # List of potenitial dataframes
            print(f"Available dataframes: {dataframes}")
            print(f"Combining {len(dataframes)} dataframes...")            
            combined_df = combine_sources(bridgedb_df, dataframes)
            print(f"Combined DataFrame: {combined_df.head()}")
            print(f"Combined DataFrame colnames: {combined_df.columns.tolist()}")
            # List of potenitail metadata 
            print(f"Available metadata: {metadata}")
            print(f"Combining {len(metadata)} metadata...")
            combined_metadata = create_or_append_to_metadata(bridgedb_metadata, metadata)

            # Create a graph from the annotated dataframe
            if opentargets_df is not None:
                pygraph = generator.save_graph(
                    combined_df=combined_df,
                    combined_metadata=combined_metadata,
                    disease_compound=opentargets_df,
                    graph_name="examples",
                    graph_dir="./data",
                )  #TODO: the save_graph function is not found in the pyBiodatafuse package, check and fix
            else:
                pygraph = generator.save_graph(
                    combined_df=combined_df,
                    combined_metadata=combined_metadata,
                    graph_name="examples",
                    graph_dir="./data",
                ) 
            print("I am here 302")

            # Store results in database
            identifier_set.combined_df = combined_df.to_dict(orient="index")
            identifier_set.combined_metadata = combined_metadata
            if opentargets_df is not None:
                identifier_set.opentargets_df = opentargets_df.to_dict(orient="index")
            
            identifier_set.pygraph = pygraph
            await self.db.commit()
            print("I am here 312")
            return combined_df, combined_metadata, pygraph, opentargets_df
            
        except Exception as e:
            raise ValueError(f"Error processing data sources: {str(e)}")

    # async def get_source_metadata(self, source_name: str) -> Dict:
    #     """Get metadata for a specific data source"""
    #     if source_name not in self.available_sources:
    #         raise ValueError(f"Unknown data source: {source_name}")
    #     return self.available_sources[source_name]
