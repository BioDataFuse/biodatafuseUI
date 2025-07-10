from io import BytesIO, StringIO
from typing import List, Optional, Tuple

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
        file_content: Optional[bytes] = None,
        input_species: str = "Human",
        column_name: Optional[str] = None,
        file_type: Optional[str] = None,  # <- ADD THIS
    ) -> models.IdentifierSet:

        identifiers, warnings = self._process_identifiers(
            text_input,
            file_content,
            column_name=column_name,
            file_type=file_type  # <- pass here too
        )

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

        if identifiers:
            try:
                ids_df = pd.DataFrame({"identifier": identifiers})

                bridgedb_df, bridgedb_metadata = id_mapper.bridgedb_xref(
                    identifiers=ids_df,
                    input_species=input_species,
                    input_datasource=identifier_type,
                    output_datasource="All",  # You can adjust the output datasource if needed
                )
                bridgedb_df.rename(
                    columns={
                        "identifier.source": "identifier_source",
                        "target.source": "target_source",
                    },
                    inplace=True,
                )
                bridgedb_subset_df = bridgedb_df[
                    bridgedb_df["target_source"].isin(
                        ["Ensembl", "NCBI Gene", "PubChem Compound", "HMDB", "ChemSpider"]
                    ) & (bridgedb_df["target"] != bridgedb_df["identifier"])
                ].sort_values(by=["identifier", "target_source"])

                print(bridgedb_subset_df.head())
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
        self,
        text_input: Optional[str] = None,
        file_content: Optional[bytes] = None,
        column_name: Optional[str] = None,
        file_type: Optional[str] = None
    ) -> Tuple[List[str], Optional[str]]:
        identifiers = []
        warnings = None

        if text_input:
            text_identifiers = [id.strip() for id in text_input.split() if id.strip()]
            identifiers.extend(text_identifiers)

        if file_content:
            try:
                if file_type and ("spreadsheetml" in file_type or "excel" in file_type):
                    df = pd.read_excel(BytesIO(file_content))
                else:
                    df = pd.read_csv(StringIO(file_content.decode("utf-8")))

                target_col = column_name or "identifier"
                if target_col in df.columns:
                    identifiers = df[target_col].dropna().astype(str).unique().tolist()
                else:
                    warnings = f"File must contain column '{target_col}'"

            except Exception as e:
                warnings = f"Error processing file: {str(e)}"

        identifiers = list(set(filter(None, identifiers)))
        if not identifiers and not warnings:
            warnings = "No valid identifiers provided"

        return identifiers, warnings

    async def get_identifier_set(self, set_id: int) -> Optional[models.IdentifierSet]:
        result = await self.db.execute(
            select(models.IdentifierSet).where(models.IdentifierSet.id == set_id)
        )
        identifier_set = result.scalar_one_or_none()
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
    