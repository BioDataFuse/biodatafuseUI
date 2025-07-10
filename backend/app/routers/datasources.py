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
async def get_available_datasources(#TODO: not being used, not sure if needed
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    """Get list of available data sources."""
    datasource_service = DataSourceService(db)
    return await datasource_service.get_available_sources()


@router.post("/{set_id}/process", response_model=DataSourceProcessingResponse)
async def annotations_from_datasources(
    set_id: int,
    datasources: List[DataSourceRequest],
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Process selected data sources for a given identifier set.

    Parameters:
        set_id (int): The ID of the identifier set to process.
        datasources (List[DataSourceRequest]): List of data sources to process, where needed with its API key and mapping name.
        current_user: The currently authenticated user (injected by FastAPI dependency).
        db (AsyncSession): The database session (injected by FastAPI dependency).

    Returns:
        DataSourceProcessingResponse: Contains the processing status, set ID, and a message.

    Raises:
        HTTPException: If the identifier set is not found, not owned by the user, no sources are provided,
                       or if an error occurs during processing.
    """

    try:
        # Verify ownership of identifier set
        identifier_service = IdentifierService(db)
        identifier_set = await identifier_service.get_identifier_set(set_id)
        if not identifier_set:
            raise HTTPException(status_code=404, detail="Identifier set not found")
        if identifier_set.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="Not authorized to access this identifier set"
            )

        # Validate data sources
        if not datasources:
            raise HTTPException(status_code=400, detail="No data sources provided")
        # Convert datasources to the format expected by the service
        datasources = [
            {"source": datasource.source, "api_key": datasource.api_key, "map_name": datasource.map_name} for datasource in datasources
        ]
        # Process selected datasources
        datasource_service = DataSourceService(db)
        annotation = await datasource_service.create_annotations_for_identifier_set(
            set_id=set_id,
            datasources=datasources,
        )

        # combined_df, combined_metadata, pygraph, opentargets_df, captured_warnings  = await datasource_service.create_annotations_for_identifier_set(
        #     set_id=set_id,
        #     datasources=datasources, 
        # )


        # if annotation.combined_df is not None:
        return DataSourceProcessingResponse(
            identifier_set_id=set_id,
            status=annotation.status,
            message="Data sources processed successfully",
            combined_df=annotation.combined_df,
            combined_metadata=annotation.combined_metadata,
            opentargets_df=annotation.opentargets_df,
            captured_warnings=annotation.captured_warnings,
            error_message=annotation.error_message,
        )
        # else:
        #     return DataSourceProcessingResponse(
        #         status=annotation.status,
        #         message="No data found from selected sources",
        #     )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing data sources: {str(e)}",
        )


