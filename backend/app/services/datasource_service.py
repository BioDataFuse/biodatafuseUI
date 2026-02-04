import asyncio
import json
import os
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
    kegg,
    aopwiki,
    intact,
    mitocarta
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
            "opentargets_disease_compound": {
                "name": f"{constants.OPENTARGETS} - Disease to compound annotation",
                "description": "Target discovery and prioritization",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.OPENTARGETS_ENDPOINT,
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
            "intact_gene_interactions": {
                "name": f"{constants.INTACT} - Molecular interaction for genes",
                "description": "Molecular interaction network",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.INTACT_ENDPOINT,
            },
            "intact_compound_interactions": {
                "name": f"{constants.INTACT} - Molecular interaction for compounds",
                "description": "Molecular interaction network",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.INTACT_ENDPOINT,
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
            "opentargets_gene_compound": {
                "name": f"{constants.OPENTARGETS} - Gene to compound annotation",
                "description": "Target discovery and prioritization",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.OPENTARGETS_ENDPOINT,
            },
            "mitocarta" : {
                "name": f"{constants.MITOCARTA}",
                "description": "Inventory of mammalian mitochondrial proteins and pathways",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.MITOCARTA_DOWNLOAD_URL,
            },
            "pubchem_assays": {
                "name": f"{constants.PUBCHEM} - Assays",
                "description": "Chemical information (molecules screened on proteins as targets)",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.PUBCHEM_ENDPOINT,
            },
            "molmedb_compounds": {
                "name": f"{constants.MOLMEDB} - Transporter inhibitor annotation (linking the compounds to inhibited genes)",
                "description": "Molecular interactions with membranes",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.MOLMEDB_ENDPOINT,
            },
            "molmedb_gene": {
                "name": f"{constants.MOLMEDB} - Transporter inhibitor annotation (linking transporters encoded by genes to their inhibitors)",
                "description": "Molecular interactions with membranes",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.MOLMEDB_ENDPOINT,
            },
            "aop_wiki_rdf": {
                "name": f"Adverse Outcome Pathways (AOP-Wiki)",
                "description": "Adverse Outcome Pathways and their components",
                "requires_key": False,
                "requires_map_name": False,
                "base_url": constants.AOPWIKI_ENDPOINT,
            }
        }

    async def get_available_sources(self) -> List[Dict]:
        """Get list of available data sources"""
        return [{"id": key, "category": self.get_source_category(key), **value} 
                for key, value in self.available_sources.items()]

    def get_source_category(self, key: str) -> str:
        if key in ["bgee", "disgenet", "opentargets_disease_compound","minerva", "wikipathways_pathways", 
                   "wikipathways_interactions", "minerva", "opentargets_go", "opentargets_reactome",
                   "stringdb", "molmedb_gene", "intact_gene_interactions", "mitocarta",
                   "opentargets_gene_compound", "pubchem_assays"]:
            return "gene"
        elif key in ["molmedb_compounds", "intact_compound_interactions"]:
            return "compound"
        elif key in ["kegg", "aop_wiki_rdf"]:
            return "both gene and compound"

    @staticmethod
    async def get_datasource_metadata() -> List[Dict]:
        """
        Get metadata (version and endpoint) for all available data sources.
        Fetches version info from pyBiodatafuse annotators where available.
        """
        import concurrent.futures
        
        from pyBiodatafuse.annotators import (
            bgee, stringdb, wikipathways, opentargets, intact
        )
        from pyBiodatafuse.annotators.kegg import check_version_kegg
        
        # Define sources with their metadata fetching functions
        sources_metadata = [
            {
                "id": "bgee",
                "name": constants.BGEE,
                "description": "Gene expression levels in different tissues",
                "endpoint": constants.BGEE_ENDPOINT,
                "get_version": bgee.get_version_bgee,
            },
            {
                "id": "disgenet",
                "name": constants.DISGENET,
                "description": "Gene-disease associations",
                "endpoint": constants.DISGENET_ENDPOINT,
                "version": None,  # Requires API key
            },
            {
                "id": "opentargets",
                "name": constants.OPENTARGETS,
                "description": "Target discovery and prioritization",
                "endpoint": constants.OPENTARGETS_ENDPOINT,
                "get_version": opentargets.get_version_opentargets,
            },
            {
                "id": "wikipathways",
                "name": constants.WIKIPATHWAYS,
                "description": "Biological pathways",
                "endpoint": constants.WIKIPATHWAYS_ENDPOINT,
                "get_version": wikipathways.get_version_wikipathways,
            },
            {
                "id": "kegg",
                "name": constants.KEGG,
                "description": "Kyoto Encyclopedia of Genes and Genomes",
                "endpoint": constants.KEGG_ENDPOINT,
                "get_version": lambda: {"source_version": check_version_kegg()},
            },
            {
                "id": "minerva",
                "name": constants.MINERVA,
                "description": "System biology networks",
                "endpoint": constants.MINERVA_ENDPOINT,
                "version": None,  # Requires map endpoint
            },
            {
                "id": "stringdb",
                "name": constants.STRING,
                "description": "Protein-protein interaction network",
                "endpoint": constants.STRING_ENDPOINT,
                "get_version": stringdb.get_version_stringdb,
            },
            {
                "id": "intact",
                "name": constants.INTACT,
                "description": "Molecular interaction network",
                "endpoint": constants.INTACT_ENDPOINT,
                "get_version": intact.check_version_intact,
            },
            {
                "id": "molmedb",
                "name": constants.MOLMEDB,
                "description": "Molecular interactions with membranes",
                "endpoint": constants.MOLMEDB_ENDPOINT,
                "version": None,
            },
            {
                "id": "pubchem",
                "name": constants.PUBCHEM,
                "description": "Chemical information",
                "endpoint": constants.PUBCHEM_ENDPOINT,
                "version": None,
            },
            {
                "id": "aopwiki",
                "name": "AOP-Wiki",
                "description": "Adverse Outcome Pathways and their components",
                "endpoint": constants.AOPWIKI_ENDPOINT,
                "version": None,
            },
            {
                "id": "mitocarta",
                "name": constants.MITOCARTA,
                "description": "Inventory of mammalian mitochondrial proteins and pathways",
                "endpoint": constants.MITOCARTA_DOWNLOAD_URL,
                "version": None,
            },
        ]
        
        def fetch_version(source):
            """Fetch version for a single source."""
            result = {
                "id": source["id"],
                "name": source["name"],
                "description": source["description"],
                "endpoint": source["endpoint"],
                "version": source.get("version"),
            }
            
            if "get_version" in source:
                try:
                    version_data = source["get_version"]()
                    if isinstance(version_data, dict):
                        if "source_version" in version_data:
                            result["version"] = version_data["source_version"]
                        elif constants.METADATA in version_data:
                            meta = version_data[constants.METADATA]
                            if isinstance(meta, dict) and "source_version" in meta:
                                sv = meta["source_version"]
                                if isinstance(sv, dict) and "apiVersion" in sv:
                                    result["version"] = sv["apiVersion"]
                                    if "data_version" in meta:
                                        result["version"] += f" (data: {meta['data_version']})"
                                else:
                                    result["version"] = str(sv)
                except Exception as e:
                    result["version"] = None
            
            return result
        
        # Use thread pool to fetch versions concurrently
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                loop.run_in_executor(executor, fetch_version, source)
                for source in sources_metadata
            ]
            results = await asyncio.gather(*futures)
        
        return results

    async def create_annotations_for_identifier_set(
        self,
        set_id: int,
        datasources: List[Dict],  # List of {source: str, api_key: Optional[str], map_name: Optional[str]}

    ) -> models.Annotation:
        identifier_set = await self.db.execute(
            select(models.IdentifierSet).where(models.IdentifierSet.id == set_id)
        )
        identifier_set = identifier_set.scalar_one_or_none()
        if not identifier_set:
            raise ValueError("Identifier set not found")
        # Create annotation for identifier set
        annotation = models.Annotation(
            identifier_set_id=set_id
        )

        self.db.add(annotation)
        await self.db.commit()
        # await self.db.refresh(annotation)
        try:
            bridgedb_df = pd.DataFrame(identifier_set.mapped_identifiers).T
            bridgedb_df = bridgedb_df.rename(columns={'identifier_source': 'identifier.source', 'target_source': 'target.source'})
            bridgedb_metadata = identifier_set.bridgedb_metadata


        except Exception as e:
            raise ValueError (f"Error loading mapped_identifiers_subset: {e}")
        if not bridgedb_df.empty:
            try:
                combined_df, combined_metadata, opentargets_df, captured_warnings = await self._process_selected_sources(
                    bridgedb_df=bridgedb_df,
                    bridgedb_metadata=bridgedb_metadata,            
                    datasources=datasources,
                )

                # Store results in database
                annotation.combined_df = combined_df.to_dict(orient="index")
                annotation.combined_metadata = combined_metadata
                if opentargets_df is not None:
                    annotation.opentargets_df = opentargets_df.to_dict(orient="index")

                # annotation.pygraph = pygraph
                annotation.captured_warnings = captured_warnings if captured_warnings else None
                annotation.status = "completed"
                await self.db.commit()
                await self.db.refresh(annotation)

            except Exception as e:
                annotation.status = "error"
                annotation.error_message = str(e)
                await self.db.commit()

            await self.db.commit()

            return annotation

    async def _process_selected_sources(
        self,
        bridgedb_df: pd.DataFrame,
        bridgedb_metadata: List[dict],
        datasources: List[Dict],  # List of {source: str, api_key: Optional[str], map_name: Optional[str]}
    ) -> Tuple[pd.DataFrame, Dict, str, pd.DataFrame, Dict]:

        """Process selected data sources"""
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
                            minerva_df, minerva_metadata = minerva.get_gene_pathways(
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
                        elif source_name == "kegg":
                            kegg_df, kegg_metadata = kegg.get_pathways(
                                bridgedb_df=bridgedb_df
                            )
                            dataframes.append(kegg_df)
                            metadata.append(kegg_metadata)
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
                            # Clean up pubchem cache file created by pyBiodatafuse
                            cache_file = "pubchem_cache_results.json"
                            if os.path.exists(cache_file):
                                try:
                                    os.remove(cache_file)
                                except Exception:
                                    pass  # Ignore cleanup errors
                        elif source_name == "molmedb_gene":
                            inhibitor_df, inhibitor_metadata = molmedb.get_gene_compound_inhibitor(bridgedb_df=bridgedb_df)
                            dataframes.append(inhibitor_df)
                            metadata.append(inhibitor_metadata)
                        elif source_name == "molmedb_compounds":
                            molmedb_transporter_inhibited_df, molmedb_transporter_inhibited_metadata = molmedb.get_compound_gene_inhibitor(bridgedb_df=bridgedb_df)
                            dataframes.append(molmedb_transporter_inhibited_df)
                            metadata.append(molmedb_transporter_inhibited_metadata)
                        elif source_name == "aop_wiki_rdf": #TODO: needs to be updated
                            aopwiki_df, aopwiki_metadata = aopwiki.get_aops(
                                bridgedb_df=bridgedb_df)
                            dataframes.append(aopwiki_df)
                            metadata.append(aopwiki_metadata)
                        elif source_name == "stringdb":
                            ppi_df, ppi_metadata = stringdb.get_ppi(bridgedb_df=bridgedb_df)
                            dataframes.append(ppi_df)
                            metadata.append(ppi_metadata)
                        elif source_name == "intact_gene_interactions":
                            intact_gene_df, intact_gene_metadata = intact.get_gene_interactions(
                                bridgedb_df=bridgedb_df
                            )
                            dataframes.append(intact_gene_df)
                            metadata.append(intact_gene_metadata)
                        elif source_name == "intact_compound_interactions":
                            intact_compound_df, intact_compound_metadata = intact.get_compound_interactions(
                                bridgedb_df=bridgedb_df
                            )
                            dataframes.append(intact_compound_df)
                            metadata.append(intact_compound_metadata)
                        elif source_name == "mitocarta":
                            mitocarta_df, mitocarta_metadata = mitocarta.get_gene_mito_pathways(
                                bridgedb_df=bridgedb_df,
                                mitocarta_file="Human.MitoCarta3.0.xls",
                                filename="human_mitocarta3.0.xls",
                                species="hsapiens",
                                sheet_name="A Human MitoCarta3.0"
                            )
                            dataframes.append(mitocarta_df)
                            metadata.append(mitocarta_metadata)
                        else:
                            continue

                    except Exception as e:
                        f"Error processing {source_name}: {str(e)}"

                        continue

            warning_messages = [str(w.message) for w in caught_warnings]

            filtered_warnings = [warning for warning in warning_messages if warning.startswith("There is no annotation for your input list")]

            # Combine all dataframes
            combined_df = combine_sources(bridgedb_df, dataframes)
            # List of potenitail metadata
            combined_metadata = create_or_append_to_metadata(bridgedb_metadata, metadata)

            # return combined_df, combined_metadata, pygraph, opentargets_df, warning_messages
            return combined_df, combined_metadata, opentargets_df, filtered_warnings            

        except Exception as e:
            raise ValueError(f"Error processing data sources: {str(e)}")

    async def get_annotations_for_identifier_set(self, set_id: int) -> Optional[models.IdentifierSet]:
        result = await self.db.execute(
            select(models.IdentifierSet).where(models.IdentifierSet.id == set_id)
        )
        annotation = result.scalar_one_or_none()
        return annotation

    # async def get_source_metadata(self, source_name: str) -> Dict:
    #     """Get metadata for a specific data source"""
    #     if source_name not in self.available_sources:
    #         raise ValueError(f"Unknown data source: {source_name}")
    #     return self.available_sources[source_name]
