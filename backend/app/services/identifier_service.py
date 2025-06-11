import json
import logging
from collections import defaultdict
from io import StringIO
from typing import Dict, List, Optional, Tuple

import pandas as pd
from pyBiodatafuse import id_mapper
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models


class IdentifierService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_identifier_set(
        self,
        user_id: int,
        identifier_type: str,
        text_input: Optional[str] = None,
        file_content: Optional[str] = None,
        input_species: str = "Human",
    ) -> models.IdentifierSet:
        # Process identifiers
        identifiers, warnings = self._process_identifiers(text_input, file_content)
        # Create new identifier set
        identifier_set = models.IdentifierSet(
            user_id=user_id,
            identifier_type=identifier_type,
            input_species=input_species,
            input_identifiers=identifiers,
            status="pending" if identifiers else "error",
            error_message=str(warnings) if warnings else None,
        )

        self.db.add(identifier_set)
        await self.db.commit()
        await self.db.refresh(identifier_set)
        # If we have valid identifiers, perform the mapping
        if identifiers:
            try:
                # Create DataFrame for BridgeDB
                ids_df = pd.DataFrame({"identifier": identifiers})

                # Perform mapping using the pyBiodatafuse package's bridgedb_xref function
                bridgedb_df, bridgedb_metadata = id_mapper.bridgedb_xref(
                    identifiers=ids_df,
                    input_species=input_species,
                    input_datasource=identifier_type,
                    output_datasource="All",  # You can adjust the output datasource if needed
                )
                print("Reply from pyBiodatafuse")
                print("bridfedb_df:")
                print(bridgedb_df)
                bridgedb_df.rename(
                    columns={
                        "identifier.source": "identifier_source",
                        "target.source": "target_source",
                    },
                    inplace=True,
                )

                bridgedb_subset_df = bridgedb_df[
                    bridgedb_df["target_source"].isin(
                        ["Ensembl", "NCBI Gene", "PubChem Compound", "ChEMBL compound"]
                    )
                ].sort_values(by=["identifier", "target_source"])
                print("bridfedb_subset_df:")
                print(bridgedb_subset_df)

                # Store the serialized mapped identifiers as a JSON string
                # identifier_set.mapped_identifiers = json.dumps(
                #     {idx: row.to_dict() for idx, row in bridgedb_df.iterrows()},
                #     indent=4,
                # )
                # identifier_set.mapped_identifiers_subset = json.dumps(
                #     {
                #         idx: row.to_dict()
                #         for idx, row in bridgedb_subset_df.head(12).iterrows()
                #     },
                #     indent=4,
                # )
                identifier_set.mapped_identifiers = bridgedb_df.to_dict(orient="index")
                identifier_set.mapped_identifiers_subset = bridgedb_subset_df.to_dict(
                    orient="index"
                )

                identifier_set.bridgedb_metadata = bridgedb_metadata
                identifier_set.mapped_identifiers_list = (
                    bridgedb_df["identifier"].unique().tolist()
                )

                identifier_set.status = "completed"
                await self.db.commit()
                await self.db.refresh(identifier_set)

            except Exception as e:
                identifier_set.status = "error"
                identifier_set.error_message = str(e)
                await self.db.commit()

        return identifier_set

    def _process_identifiers(
        self, text_input: Optional[str] = None, file_content: Optional[str] = None
    ) -> Tuple[List[str], Optional[str]]:
        identifiers = []
        warnings = None
        # Process text input
        if text_input:
            text_identifiers = [id.strip() for id in text_input.split() if id.strip()]
            identifiers.extend(text_identifiers)

        # Process file content
        if file_content:
            try:
                df = pd.read_csv(StringIO(file_content))
                if "identifier" in df.columns:
                    file_identifiers = df["identifier"].dropna().unique().tolist()
                    identifiers.extend(file_identifiers)
                else:
                    warnings = "File must contain 'identifier' column"
            except Exception as e:
                warnings = f"Error processing file: {str(e)}"

        # Remove duplicates and empty strings
        identifiers = list(set(filter(None, identifiers)))

        if not identifiers and not warnings:
            warnings = "No valid identifiers provided"

        return identifiers, warnings

    async def get_identifier_set(self, set_id: int) -> Optional[models.IdentifierSet]:
        result = await self.db.execute(
            select(models.IdentifierSet).where(models.IdentifierSet.id == set_id)
        )
        identifier_set = result.scalar_one_or_none()

        if identifier_set:
            if identifier_set.mapped_identifiers:
                identifier_set.mapped_identifiers = identifier_set.mapped_identifiers
            if identifier_set.mapped_identifiers_subset:
                identifier_set.mapped_identifiers_subset = (
                    identifier_set.mapped_identifiers_subset
                )
            if identifier_set.bridgedb_metadata:
                identifier_set.bridgedb_metadata = identifier_set.bridgedb_metadata
            if identifier_set.mapped_identifiers_list:
                identifier_set.mapped_identifiers_list = (
                    identifier_set.mapped_identifiers_list
                )
        return identifier_set

    async def get_user_identifier_sets(
        self, user_id: int
    ) -> List[models.IdentifierSet]:
        result = await self.db.execute(
            select(models.IdentifierSet)
            .where(models.IdentifierSet.user_id == user_id)
            .order_by(models.IdentifierSet.created_at.desc())
        )
        return result.scalars().all()
