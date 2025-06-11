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
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    print("Starting function: process_identifiers")
    identifier_service = IdentifierService(db)
    print("Step 1")
    file_content = None
    if file:
        file_content = await file.read()
        file_content = file_content.decode()

    identifier_set = await identifier_service.create_identifier_set(
        user_id=current_user.id,
        identifier_type=identifier_type,
        text_input=text_input,
        file_content=file_content,
        input_species=input_species,
    )
    print("Ending function process_identifiers")
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
    print(f"Starting function: get_identifier_mapping")
    identifier_service = IdentifierService(db)

    identifier_set = await identifier_service.get_identifier_set(set_id)
    print(f"identifier_set: {identifier_set}")

    if not identifier_set:
        raise HTTPException(status_code=404, detail="Identifier set not found")

    if identifier_set.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this identifier set"
        )
    print(f"Ending function: get_identifier_mapping")
    return identifier_set


@router.get("", response_model=List[schemas.IdentifierMappingResponse])
async def list_identifier_sets(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    identifier_service = IdentifierService(db)
    return await identifier_service.get_user_identifier_sets(current_user.id)
