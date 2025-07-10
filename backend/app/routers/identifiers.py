from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas
from ..database import get_db
from ..services.identifier_service import IdentifierService
from .auth import get_current_user

router = APIRouter(prefix="/identifiers", tags=["Identifiers"])


@router.post("", response_model=schemas.IdentifierProcessingResponse)
async def process_identifiers(
    identifier_type: str = Form(...),
    text_input: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    input_species: str = Form("Human"),
    column_name: Optional[str] = Form(None),
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Process identifiers from text input or file upload.
    Processes user-submitted identifiers via form data or file upload.
    This asynchronous endpoint handles the submission of identifiers for processing.
    Users can provide identifiers either as text input or by uploading a file. The
    function creates an identifier set associated with the current user and initiates
    processing based on the provided identifier type and species.
    Args:
        identifier_type (str): The type of identifiers being submitted (e.g., gene, protein).
        text_input (Optional[str]): Identifiers provided as plain text input (optional).
        file (Optional[UploadFile]): File containing identifiers to be processed (optional).
        input_species (str): The species context for the identifiers (default is "Human").
        current_user: The currently authenticated user (injected by FastAPI dependency).
        db (AsyncSession): The database session (injected by FastAPI dependency).
    Returns:
        schemas.IdentifierProcessingResponse: Response object containing the identifier set ID,
        processing status, a message, and any warnings or error messages.
    Raises:
        HTTPException: If there is an error during identifier set creation or processing.
    """
    identifier_service = IdentifierService(db)
    file_content = None
    if file:
        file_content = await file.read()  # <- this is bytes
        file_type = file.content_type
    else:
        file_content = None
        file_type = None

    identifier_set = await identifier_service.create_identifier_set(
        user_id=current_user.id,
        identifier_type=identifier_type,
        text_input=text_input,
        file_content=file_content,
        input_species=input_species,
        column_name=column_name,
        file_type=file_type
    )
    return schemas.IdentifierProcessingResponse(
        set_id=identifier_set.id,
        status=identifier_set.status,
        message=(
            "Identifiers received and processing started"
            if identifier_set.status == "pending"
            else "Error processing identifiers"
        ),
        warnings=(
            [identifier_set.error_message] if identifier_set.error_message else None
        ),
    )


@router.get("/{set_id}", response_model=schemas.IdentifierMappingResponse)
async def get_identifier_mapping(
    set_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    identifier_service = IdentifierService(db)

    identifier_set = await identifier_service.get_identifier_set(set_id)

    if not identifier_set:
        raise HTTPException(status_code=404, detail="Identifier set not found")

    if identifier_set.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this identifier set"
        )
    return identifier_set


@router.get("", response_model=List[schemas.IdentifierMappingResponse])
async def list_identifier_sets(#TODO: not sure if this is needed
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    identifier_service = IdentifierService(db)
    return await identifier_service.get_user_identifier_sets(current_user.id)
