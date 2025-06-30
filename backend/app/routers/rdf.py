from typing import Dict, List, Optional
import os
import tempfile
import uuid
from pathlib import Path
import logging

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..schemas import RDFGenerationRequest, RDFGenerationResponse
from ..services.rdf_service import RDFService
from .auth import get_current_user

router = APIRouter(prefix="/rdf", tags=["RDF Generation"])

logger = logging.getLogger("rdf_router")


@router.post("/generate", response_model=RDFGenerationResponse)
async def generate_rdf(
    request: RDFGenerationRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Generate RDF graph from annotation data."""
    try:
        logger.info(f"🔧 Starting RDF generation for user {current_user.id}")
        
        rdf_service = RDFService(db)
        result = await rdf_service.generate_rdf_graph(
            identifier_set_id=request.identifier_set_id,
            base_uri=request.base_uri,
            version_iri=request.version_iri,
            author_name=request.author_name,
            author_email=request.author_email,
            orcid=request.orcid,
            graph_name=request.graph_name,
            generate_shacl=request.generate_shacl,
            shacl_threshold=request.shacl_threshold,
            generate_uml_diagram=request.generate_uml_diagram,
            generate_shex=request.generate_shex,
            shex_threshold=request.shex_threshold,
            user_id=current_user.id,
        )
        
        logger.info(f"✅ RDF generation completed successfully")
        return result
        
    except Exception as e:
        logger.error(f"❌ Error in RDF generation endpoint: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/download/{file_id}")
async def download_rdf_file(
    file_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Download generated RDF file."""
    try:
        rdf_service = RDFService(db)
        file_info = await rdf_service.get_file_info(file_id, current_user.id)
        
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_path = Path(file_info["path"])
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on disk")
        
        # Determine media type based on file extension
        if file_path.suffix.lower() == '.png':
            media_type = "image/png"
        elif file_path.suffix.lower() in ['.ttl', '.turtle']:
            media_type = "text/turtle"
        else:
            media_type = "application/octet-stream"
        
        return FileResponse(
            path=str(file_path),
            filename=file_info["name"],
            media_type=media_type
        )
        
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/preview/{file_id}")
async def preview_rdf_file(
    file_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Preview generated RDF file (for images)."""
    try:
        rdf_service = RDFService(db)
        file_info = await rdf_service.get_file_info(file_id, current_user.id)
        
        if not file_info:
            raise HTTPException(status_code=404, detail="File not found")
        
        file_path = Path(file_info["path"])
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found on disk")
        
        # Only serve image files for preview
        if file_path.suffix.lower() not in ['.png', '.jpg', '.jpeg', '.svg']:
            raise HTTPException(status_code=400, detail="File type not supported for preview")
        
        # Determine media type based on file extension
        if file_path.suffix.lower() == '.png':
            media_type = "image/png"
        elif file_path.suffix.lower() in ['.jpg', '.jpeg']:
            media_type = "image/jpeg"
        elif file_path.suffix.lower() == '.svg':
            media_type = "image/svg+xml"
        else:
            media_type = "image/png"
        
        return FileResponse(
            path=str(file_path),
            media_type=media_type
        )
        
    except Exception as e:
        logger.error(f"Error previewing file {file_id}: {str(e)}")
        raise HTTPException(status_code=404, detail="File not found or cannot be previewed")
