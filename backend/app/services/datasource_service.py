from typing import Dict, List, Tuple, Optional
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models
from pyBiodatafuse.annotators import wikipathways, disgenet, opentargets, stringdb
from pyBiodatafuse.utils import combine_sources
import asyncio

class DataSourceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.available_sources = {
            "disgenet": {
                "name": "DisGeNET",
                "description": "Gene-disease associations database",
                "requires_key": True
            },
            "string": {
                "name": "STRING",
                "description": "Protein-protein interaction network",
                "requires_key": False
            },
            "wikipathways": {
                "name": "WikiPathways",
                "description": "Biological pathway database",
                "requires_key": False
            },
            "opentarget.gene_ontology": {
                "name": "OpenTargets Gene Ontology",
                "description": "Gene ontology process annotations",
                "requires_key": False
            },
            "opentarget.reactome": {
                "name": "OpenTargets Reactome",
                "description": "Reactome pathway associations",
                "requires_key": False
            },
            "opentarget.drug_interactions": {
                "name": "OpenTargets Drug Interactions",
                "description": "Gene-drug interaction data",
                "requires_key": False
            },
            "opentarget.disease_associations": {
                "name": "OpenTargets Disease Associations",
                "description": "Gene-disease association data",
                "requires_key": False
            }
        }

        # Map sources to their corresponding functions
        self.data_source_functions = {
            "disgenet": disgenet.get_gene_disease,
            "opentarget.gene_ontology": opentargets.get_gene_go_process,
            "opentarget.reactome": opentargets.get_gene_reactome_pathways,
            # "opentarget.drug_interactions": opentargets.get_gene_drug_interactions,
            "opentarget.disease_associations": opentargets.get_gene_disease_associations,
            "string": stringdb.get_ppi,
            "wikipathways": wikipathways.get_gene_wikipathways
        }

    async def get_available_sources(self) -> List[Dict]:
        """Get list of available data sources"""
        return [
            {"id": key, **value}
            for key, value in self.available_sources.items()
        ]

    async def process_selected_sources(
        self,
        identifier_set_id: int,
        datasources: List[Dict],  # List of {source: str, api_key: Optional[str]}
    ) -> Tuple[pd.DataFrame, Dict]:
        """Process selected data sources with their API keys"""
        identifier_set = await self.db.execute(
            select(models.IdentifierSet).where(models.IdentifierSet.id == identifier_set_id)
        )
        identifier_set = identifier_set.scalar_one_or_none()
        
        if not identifier_set:
            raise ValueError("Identifier set not found")

        # Convert mapped identifiers to DataFrame
        bridgedb_df = pd.DataFrame(identifier_set.mapped_identifiers)

        # Initialize variables for combined results
        combined_data = pd.DataFrame()
        combined_metadata = {}
        warnings = []
        
        try:
            # Process each selected data source
            for source_info in datasources:
                source_name = source_info["source"]
                api_key = source_info.get("api_key")

                if source_name not in self.data_source_functions:
                    warnings.append(f"Unsupported data source: {source_name}")
                    continue

                # Process the data source
                try:
                    if source_name == "disgenet":
                        tmp_data, tmp_metadata = await asyncio.to_thread(
                            self.data_source_functions[source_name],
                            api_key=api_key,
                            bridgedb_df=bridgedb_df
                        )
                    else:
                        tmp_data, tmp_metadata = await asyncio.to_thread(
                            self.data_source_functions[source_name],
                            bridgedb_df
                        )

                    combined_metadata[source_name] = tmp_metadata

                    if tmp_data.empty:
                        warnings.append(f"No annotation available for {source_name}")
                    else:
                        if combined_data.empty:
                            combined_data = tmp_data
                        else:
                            combined_data = combine_sources(bridgedb_df, [combined_data, tmp_data])

                except Exception as e:
                    warnings.append(f"Error processing {source_name}: {str(e)}")
                    continue

            # Prepare metadata for response
            metadata = {
                "total_associations": len(combined_data) if not combined_data.empty else 0,
                "sources_processed": list(combined_metadata.keys()),
                "source_counts": {
                    source: metadata.get("count", 0) 
                    for source, metadata in combined_metadata.items()
                },
                "warnings": warnings
            }

            # Store results in database
            identifier_set.combined_data = combined_data.to_dict("records") if not combined_data.empty else []
            identifier_set.metadata.update(metadata)
            await self.db.commit()

            return combined_data, metadata

        except Exception as e:
            raise ValueError(f"Error processing data sources: {str(e)}")

    async def get_source_metadata(self, source_name: str) -> Dict:
        """Get metadata for a specific data source"""
        if source_name not in self.available_sources:
            raise ValueError(f"Unknown data source: {source_name}")
        return self.available_sources[source_name]