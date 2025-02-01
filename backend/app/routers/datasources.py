from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Optional
from ..database import get_db
from ..services.datasource_service import DataSourceService
from ..services.identifier_service import IdentifierService
from .auth import get_current_user
from ..schemas import DataSourceRequest

router = APIRouter(prefix="/datasources", tags=["Data Sources"])


@router.get("", response_model=List[Dict])
async def get_available_datasources(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    datasource_service = DataSourceService(db)
    return await datasource_service.get_available_sources()

@router.post("/{identifier_set_id}/process")
async def process_datasources(
    identifier_set_id: int,
    datasources: List[DataSourceRequest],
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify ownership of identifier set
    identifier_service = IdentifierService(db)
    identifier_set = await identifier_service.get_identifier_set(identifier_set_id)
    
    if not identifier_set:
        raise HTTPException(status_code=404, detail="Identifier set not found")
    
    if identifier_set.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this identifier set")

    # Extract sources and create API key mapping
    selected_sources = [ds.source for ds in datasources]
    api_keys = {ds.source: ds.api_key for ds in datasources if ds.api_key}

    # Check if DisGeNET is selected and API key is provided
    if "disgenet" in selected_sources and not api_keys.get("disgenet"):
        raise HTTPException(
            status_code=400,
            detail="API key required for DisGeNET datasource"
        )

    # Process selected sources
    datasource_service = DataSourceService(db)
    try:
        _, metadata = await datasource_service.process_selected_sources(
            identifier_set_id,
            selected_sources,
            api_keys
        )
        return {
            "status": "success",
            "metadata": metadata,
            "message": "Data sources processed successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))