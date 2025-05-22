from typing import Dict, List, Tuple, Optional
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models
from pyBiodatafuse.annotators import wikipathways
from pyBiodatafuse.utils import combine_sources
import aiohttp
import asyncio
import json
from datetime import datetime

class DataSourceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.available_sources = {
            "disgenet": {
                "name": "DisGeNET",
                "description": "Gene-disease associations database",
                "requires_key": True,
                "base_url": "https://www.disgenet.org/api"
            },
            # "string": {
            #     "name": "STRING",
            #     "description": "Protein-protein interaction network",
            #     "requires_key": False,
            #     "base_url": "https://string-db.org/api"
            # },
            "wikipathways": {
                "name": "WikiPathways",
                "description": "Biological pathway database",
                "requires_key": False,
                "base_url": "https://webservice.wikipathways.org"
            },
            # "opentargets": {
            #     "name": "OpenTargets",
            #     "description": "Target validation platform",
            #     "requires_key": False,
            #     "base_url": "https://api.platform.opentargets.org/api/v4/graphql"
            # }
        }

    async def get_available_sources(self) -> List[Dict]:
        """Get list of available data sources"""
        return [
            {"id": key, **value}
            for key, value in self.available_sources.items()
        ]

    async def process_selected_sources(
        self,
        set_id: int,
        datasources: List[Dict],  # List of {source: str, api_key: Optional[str]}
    ) -> Tuple[pd.DataFrame, Dict]:
        print(f"Starting processing for identifier set ID: {set_id}")
        print(f"Datasources to process: {datasources}")

        """Process selected data sources with their API keys"""
        identifier_set = await self.db.execute(
            select(models.IdentifierSet).where(models.IdentifierSet.id == set_id)
        )
        identifier_set = identifier_set.scalar_one_or_none()
        
        if not identifier_set:
            print(f"Identifier set {set_id} not found.")

            raise ValueError("Identifier set not found")
        print(f"Fetched identifier set: {identifier_set}")

        # Convert mapped identifiers to DataFrame
        try:
            bridgedb_json = identifier_set.mapped_identifiers_subset
            bridgedb_df = pd.DataFrame(bridgedb_json)
            print(f"Bridgedb DataFrame: {bridgedb_df.head()}")
        except Exception as e:
            print(f"Error loading mapped_identifiers_subset: {e}")
            raise
        # Initialize variables for combined results
        dataframes = []
        metadata = {
            "sources_processed": [],
            "source_counts": {},
            "warnings": []
        }
        
        try:
            # Process each selected data source
            for source_info in datasources:
                source_name = source_info["source"]
                api_key = source_info.get("api_key")

                if source_name not in self.available_sources:
                    metadata["warnings"].append(f"Unsupported data source: {source_name}")
                    continue
                try:
                    if source_name == "disgenet":
                        df, source_metadata = await self.fetch_disgenet_data(
                            bridgedb_df["id"].tolist(),
                            api_key
                        )
                    # elif source_name == "string":
                    #     df, source_metadata = await self.fetch_string_data(
                    #         bridgedb_df["id"].tolist()
                    #     )
                    elif source_name == "wikipathways":
                        df, source_metadata = wikipathways.get_gene_wikipathways(
                            bridgedb_df=bridgedb_df
                        )
                    # elif source_name == "opentargets":
                    #     df, source_metadata = await self.fetch_opentargets_data(
                    #         bridgedb_df["id"].tolist()
                    #     )
                    else:
                        continue

                    metadata["sources_processed"].append(source_name)
                    metadata["source_counts"][source_name] = source_metadata["count"]
                    
                    if not df.empty:
                        dataframes.append(df)
                    else:
                        metadata["warnings"].append(f"No data found for {source_name}")

                except Exception as e:
                    metadata["warnings"].append(f"Error processing {source_name}: {str(e)}")
                    continue

            # Combine all dataframes
            print(f"Combining {len(dataframes)} dataframes...")
            combined_data = combine_sources(dataframes, bridgedb_df)
            print(f"Combined data shape: {combined_data.shape}")
            # Update metadata
            metadata["total_associations"] = len(combined_data) if not combined_data.empty else 0

            # Store results in database
            identifier_set.combined_data = json.dumps(combined_data.to_dict("records")) if not combined_data.empty else json.dumps([])
            identifier_set.metadata(metadata)
            await self.db.commit()

            return combined_data, metadata

        except Exception as e:
            raise ValueError(f"Error processing data sources: {str(e)}")

    async def get_source_metadata(self, source_name: str) -> Dict:
        """Get metadata for a specific data source"""
        if source_name not in self.available_sources:
            raise ValueError(f"Unknown data source: {source_name}")
        return self.available_sources[source_name]