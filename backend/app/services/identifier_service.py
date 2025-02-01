from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Tuple, Optional, Dict
from .. import models
from .bridgedb_service import BridgeDBService
import pandas as pd
from io import StringIO
import json

class IdentifierService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.bridgedb = BridgeDBService()

    async def create_identifier_set(
        self,
        user_id: int,
        identifier_type: str,
        text_input: Optional[str] = None,
        file_content: Optional[str] = None,
        input_species: str = "Human"
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
            error_message=str(warnings) if warnings else None
        )
        
        self.db.add(identifier_set)
        await self.db.commit()
        await self.db.refresh(identifier_set)

        # If we have valid identifiers, perform the mapping
        if identifiers:
            try:
                # Create DataFrame for BridgeDB
                ids_df = pd.DataFrame({"identifier": identifiers})
                
                # Perform BridgeDB mapping
                bridgedb_df, bridgedb_metadata = await self.bridgedb.xref_mapping(
                    identifiers=identifiers,
                    input_species=input_species,
                    input_datasource=identifier_type
                )

                # Update identifier set with mapped data
                identifier_set.mapped_identifiers = bridgedb_df.to_dict(orient="records")
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
        file_content: Optional[str] = None
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
                if 'identifier' in df.columns:
                    file_identifiers = df['identifier'].dropna().unique().tolist()
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
        return result.scalar_one_or_none()

    async def get_user_identifier_sets(self, user_id: int) -> List[models.IdentifierSet]:
        result = await self.db.execute(
            select(models.IdentifierSet)
            .where(models.IdentifierSet.user_id == user_id)
            .order_by(models.IdentifierSet.created_at.desc())
        )
        return result.scalars().all()

    async def get_supported_datasources(self, species: str = "Human") -> List[Dict]:
        """Get supported datasources for mapping"""
        return await self.bridgedb.get_supported_datasources(species)