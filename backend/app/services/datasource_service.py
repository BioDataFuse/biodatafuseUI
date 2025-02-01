from typing import Dict, List, Tuple, Optional
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .. import models
from pyBiodatafuse.datasources import DisGeNETDataSource, STRINGDataSource, KEGGDataSource
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
            "kegg": {
                "name": "KEGG",
                "description": "Pathway database",
                "requires_key": False
            }
        }

    async def get_available_sources(self) -> List[Dict]:
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
        mappings_df = pd.DataFrame(identifier_set.mapped_identifiers)
        
        combined_data = []
        metadata = {
            "total_associations": 0,
            "sources_processed": [],
            "source_counts": {}
        }

        try:
            # Process each data source
            for source_info in datasources:
                source_name = source_info["source"]
                api_key = source_info.get("api_key")

                if source_name == "disgenet":
                    data = await self._process_disgenet(mappings_df, api_key)
                elif source_name == "string":
                    data = await self._process_string(mappings_df)
                elif source_name == "kegg":
                    data = await self._process_kegg(mappings_df)
                else:
                    continue

                if data:
                    combined_data.extend(data)
                    metadata["sources_processed"].append(source_name)
                    metadata["source_counts"][source_name] = len(data)
                    metadata["total_associations"] += len(data)

            # Convert to DataFrame and remove duplicates
            result_df = pd.DataFrame(combined_data).drop_duplicates()
            
            # Store results in database
            identifier_set.combined_data = result_df.to_dict("records")
            identifier_set.metadata.update(metadata)
            await self.db.commit()

            return result_df, metadata

        except Exception as e:
            raise ValueError(f"Error processing data sources: {str(e)}")

    async def _process_disgenet(self, mappings_df: pd.DataFrame, api_key: str) -> List[Dict]:
        """Process DisGeNET data using pyBiodatafuse"""
        try:
            # Initialize DisGeNET data source
            disgenet = DisGeNETDataSource(api_key=api_key)
            
            # Get gene identifiers (prefer NCBI Gene IDs)
            gene_ids = mappings_df['ncbi'].dropna().tolist() if 'ncbi' in mappings_df.columns else mappings_df['input_id'].tolist()

            # Query DisGeNET asynchronously
            # Note: We'll simulate async here since pyBiodatafuse might not be async
            associations = await asyncio.to_thread(
                disgenet.get_gene_disease_associations,
                gene_ids
            )

            # Format results
            results = []
            for assoc in associations:
                results.append({
                    "source": "DisGeNET",
                    "gene_id": assoc.gene_id,
                    "gene_symbol": assoc.gene_symbol,
                    "disease_id": assoc.disease_id,
                    "disease_name": assoc.disease_name,
                    "score": assoc.score,
                    "evidence": assoc.evidence_count
                })

            return results
        except Exception as e:
            raise ValueError(f"Error processing DisGeNET data: {str(e)}")

    async def _process_string(self, mappings_df: pd.DataFrame) -> List[Dict]:
        """Process STRING data using pyBiodatafuse"""
        try:
            # Initialize STRING data source
            string_db = STRINGDataSource()
            
            # Get protein IDs (prefer UniProt IDs)
            protein_ids = mappings_df['uniprot'].dropna().tolist() if 'uniprot' in mappings_df.columns else mappings_df['input_id'].tolist()

            # Query STRING asynchronously
            interactions = await asyncio.to_thread(
                string_db.get_protein_interactions,
                protein_ids,
                score_threshold=0.7  # High confidence
            )

            # Format results
            results = []
            for inter in interactions:
                results.append({
                    "source": "STRING",
                    "protein_a": inter.protein_a,
                    "protein_b": inter.protein_b,
                    "score": inter.combined_score,
                    "interaction_types": inter.interaction_types
                })

            return results
        except Exception as e:
            raise ValueError(f"Error processing STRING data: {str(e)}")

    async def _process_kegg(self, mappings_df: pd.DataFrame) -> List[Dict]:
        """Process KEGG data using pyBiodatafuse"""
        try:
            # Initialize KEGG data source
            kegg = KEGGDataSource()
            
            # Get gene IDs (prefer NCBI Gene IDs)
            gene_ids = mappings_df['ncbi'].dropna().tolist() if 'ncbi' in mappings_df.columns else mappings_df['input_id'].tolist()

            # Query KEGG asynchronously
            pathways = await asyncio.to_thread(
                kegg.get_pathways,
                gene_ids
            )

            # Format results
            results = []
            for pathway in pathways:
                results.append({
                    "source": "KEGG",
                    "gene_id": pathway.gene_id,
                    "pathway_id": pathway.pathway_id,
                    "pathway_name": pathway.pathway_name,
                    "pathway_class": pathway.pathway_class
                })

            return results
        except Exception as e:
            raise ValueError(f"Error processing KEGG data: {str(e)}")
