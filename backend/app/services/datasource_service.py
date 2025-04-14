from typing import Dict, List, Tuple, Optional
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models
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
            "string": {
                "name": "STRING",
                "description": "Protein-protein interaction network",
                "requires_key": False,
                "base_url": "https://string-db.org/api"
            },
            "wikipathways": {
                "name": "WikiPathways",
                "description": "Biological pathway database",
                "requires_key": False,
                "base_url": "https://webservice.wikipathways.org"
            },
            "opentargets": {
                "name": "OpenTargets",
                "description": "Target validation platform",
                "requires_key": False,
                "base_url": "https://api.platform.opentargets.org/api/v4/graphql"
            }
        }

    async def get_available_sources(self) -> List[Dict]:
        """Get list of available data sources"""
        return [
            {"id": key, **value}
            for key, value in self.available_sources.items()
        ]

    async def fetch_disgenet_data(self, gene_ids: List[str], api_key: str) -> Tuple[pd.DataFrame, Dict]:
        """Fetch gene-disease associations from DisGeNET"""
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            results = []
            for gene_id in gene_ids:
                url = f"{self.available_sources['disgenet']['base_url']}/gda/gene/{gene_id}"
                try:
                    async with session.get(url, headers=headers) as response:
                        if response.status == 200:
                            data = await response.json()
                            results.extend(data)
                except Exception as e:
                    print(f"Error fetching DisGeNET data for {gene_id}: {str(e)}")
                    
            df = pd.DataFrame(results)
            metadata = {"count": len(results), "timestamp": datetime.now().isoformat()}
            return df, metadata

    async def fetch_string_data(self, gene_ids: List[str]) -> Tuple[pd.DataFrame, Dict]:
        """Fetch protein-protein interactions from STRING"""
        async with aiohttp.ClientSession() as session:
            results = []
            for gene_id in gene_ids:
                params = {
                    "identifiers": gene_id,
                    "species": 9606,  # Human
                    "required_score": 400,
                    "network_type": "functional"
                }
                url = f"{self.available_sources['string']['base_url']}/network"
                try:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            results.extend(data)
                except Exception as e:
                    print(f"Error fetching STRING data for {gene_id}: {str(e)}")
                    
            df = pd.DataFrame(results)
            metadata = {"count": len(results), "timestamp": datetime.now().isoformat()}
            return df, metadata

    async def fetch_wikipathways_data(self, gene_ids: List[str]) -> Tuple[pd.DataFrame, Dict]:
        """Fetch pathway data from WikiPathways"""
        async with aiohttp.ClientSession() as session:
            results = []
            for gene_id in gene_ids:
                url = f"{self.available_sources['wikipathways']['base_url']}/findPathwaysByXref"
                params = {"xref": gene_id}
                try:
                    async with session.get(url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            results.extend(data)
                except Exception as e:
                    print(f"Error fetching WikiPathways data for {gene_id}: {str(e)}")
                    
            df = pd.DataFrame(results)
            metadata = {"count": len(results), "timestamp": datetime.now().isoformat()}
            return df, metadata

    async def fetch_opentargets_data(self, gene_ids: List[str]) -> Tuple[pd.DataFrame, Dict]:
        """Fetch data from OpenTargets Platform"""
        async with aiohttp.ClientSession() as session:
            results = []
            query = """
            query targetInfo($ensemblId: String!) {
              target(ensemblId: $ensemblId) {
                id
                approvedSymbol
                goTerms {
                  id
                  name
                  aspect
                }
                pathways {
                  name
                  id
                }
                knownDrugs {
                  rows {
                    phase
                    drugId
                    drugName
                  }
                }
              }
            }
            """
            
            for gene_id in gene_ids:
                try:
                    async with session.post(
                        self.available_sources['opentargets']['base_url'],
                        json={"query": query, "variables": {"ensemblId": gene_id}}
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            if "data" in data and "target" in data["data"]:
                                results.append(data["data"]["target"])
                except Exception as e:
                    print(f"Error fetching OpenTargets data for {gene_id}: {str(e)}")
                    
            df = pd.DataFrame(results)
            metadata = {"count": len(results), "timestamp": datetime.now().isoformat()}
            return df, metadata

    def combine_dataframes(self, dfs: List[pd.DataFrame], identifier_df: pd.DataFrame) -> pd.DataFrame:
        """Combine multiple dataframes with the original identifier mapping"""
        if not dfs:
            return pd.DataFrame()
            
        result = identifier_df.copy()
        for df in dfs:
            if not df.empty:
                result = result.merge(df, how='left', on='id')
        return result

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
                    elif source_name == "string":
                        df, source_metadata = await self.fetch_string_data(
                            bridgedb_df["id"].tolist()
                        )
                    elif source_name == "wikipathways":
                        df, source_metadata = await self.fetch_wikipathways_data(
                            bridgedb_df["id"].tolist()
                        )
                    elif source_name == "opentargets":
                        df, source_metadata = await self.fetch_opentargets_data(
                            bridgedb_df["id"].tolist()
                        )
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
            combined_data = self.combine_dataframes(dataframes, bridgedb_df)
            
            # Update metadata
            metadata["total_associations"] = len(combined_data) if not combined_data.empty else 0

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