from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas import DataSourceProcessingResponse, DataSourceRequest
from ..services.datasource_service import DataSourceService
from ..services.identifier_service import IdentifierService
from .auth import get_current_user

router = APIRouter(prefix="/datasources", tags=["Data Sources"])


@router.get("", response_model=List[Dict])
async def get_available_datasources(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Get list of available data sources."""
    datasource_service = DataSourceService(db)
    print(
        "datasource_service.get_available_sources: ",
        await datasource_service.get_available_sources(),
    )
    return await datasource_service.get_available_sources()


@router.post("/{set_id}/process", response_model=DataSourceProcessingResponse)
async def process_datasources(
    set_id: int,
    sources: List[DataSourceRequest],
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Process selected data sources for a given identifier set.

    Args:
        set_id: ID of the identifier set to process
        sources: List of data sources to process with their API keys
        current_user: Current authenticated user
        db: Database session

    Returns:
        DataSourceProcessingResponse: Processing results and metadata
    """
    print(f"Starting  /{set_id}/process function")
    try:
        print(f"DB session in process_datasources: {db}")

        # Verify ownership of identifier set
        identifier_service = IdentifierService(db)
        print(f"Processing set_id: {set_id}")
        identifier_set = await identifier_service.get_identifier_set(set_id)

        print(f"Fetched identifier_set and now back: {identifier_set}")

        if not identifier_set:
            raise HTTPException(status_code=404, detail="Identifier set not found")

        if identifier_set.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not authorized to access this identifier set"
            )

        # Validate data sources
        if not sources:
            raise HTTPException(status_code=400, detail="No data sources provided")
        # Convert sources to the format expected by the service
        datasources = [
            {"source": source.source, "api_key": source.api_key} for source in sources
        ]
        print(f"db at this point: {db}")
        # Process selected sources
        datasource_service = DataSourceService(db)

        print(f"Selected datasources: {datasources}")
        processing_result, metadata = await datasource_service.process_selected_sources(
            set_id=set_id,
            datasources=datasources,  # Using the correct parameter name
        )

        print(f"Processing result: {processing_result}")
        print(f"Metadata: {metadata}")

        if not processing_result.empty:
            return DataSourceProcessingResponse(
                status="success",
                metadata=metadata,
                message="Data sources processed successfully",
            )
        else:
            return DataSourceProcessingResponse(
                status="warning",
                metadata=metadata,
                message="No data found from selected sources",
            )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing data sources: {str(e)}",
        )
