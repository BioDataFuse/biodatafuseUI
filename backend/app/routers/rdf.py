from typing import Dict, List, Optional
import os
import tempfile
import uuid
from pathlib import Path
import logging

from fastapi import APIRouter, Depends, HTTPException, Response
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
        # Debug: log the incoming request data
        logger.info(f"Received RDF generation request: {request}")
        logger.info(f"Request dict: {request.dict()}")
        logger.info(f"Current user: {getattr(current_user, 'id', None)}")
        
        rdf_service = RDFService(db)
        
        identifier_set_id = request.identifier_set_id
        logger.info(f"identifier_set_id raw: {identifier_set_id} (type: {type(identifier_set_id)})")
        if identifier_set_id is None or (isinstance(identifier_set_id, str) and not identifier_set_id.isdigit()):
            logger.error(f"Invalid identifier_set_id: {identifier_set_id}")
            raise HTTPException(status_code=400, detail="identifier_set_id must be a valid integer")
        if isinstance(identifier_set_id, str):
            identifier_set_id = int(identifier_set_id)
        if not isinstance(identifier_set_id, int):
            logger.error(f"identifier_set_id is not int after conversion: {identifier_set_id}")
            raise HTTPException(status_code=400, detail="identifier_set_id must be an integer")
        
        logger.info("Calling generate_rdf_graph with params:")
        logger.info(f"  identifier_set_id={identifier_set_id}")
        logger.info(f"  base_uri={request.base_uri}")
        logger.info(f"  version_iri={request.version_iri}")
        logger.info(f"  author_name={request.author_name}")
        logger.info(f"  author_email={request.author_email}")
        logger.info(f"  orcid={request.orcid}")
        logger.info(f"  graph_name={request.graph_name}")
        logger.info(f"  generate_shacl={request.generate_shacl}")
        logger.info(f"  shacl_threshold={request.shacl_threshold}")
        logger.info(f"  generate_uml_diagram={request.generate_uml_diagram}")
        logger.info(f"  user_id={current_user.id}")

        result = await rdf_service.generate_rdf_graph(
            identifier_set_id=identifier_set_id,
            base_uri=request.base_uri,
            version_iri=request.version_iri,
            author_name=request.author_name,
            author_email=request.author_email,
            orcid=request.orcid,
            graph_name=request.graph_name,
            generate_shacl=request.generate_shacl,
            shacl_threshold=request.shacl_threshold,
            generate_uml_diagram=request.generate_uml_diagram,
            user_id=current_user.id,
        )
        
        logger.info("RDF generation successful.")
        return result
        
    except HTTPException as e:
        logger.error(f"HTTPException: {e.detail}")
        raise e
    except Exception as e:
        logger.exception("Unhandled exception during RDF generation")
        raise HTTPException(
            status_code=400,
            detail=f"Error generating RDF: {str(e)}",
        )


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
            import logging
            logging.error(f"File info not found for file_id={file_id}, user_id={current_user.id}")
            raise HTTPException(status_code=404, detail="File not found")
        
        file_path = Path(file_info["path"])
        if not file_path.exists():
            import logging
            logging.error(f"File path does not exist: {file_path}")
            raise HTTPException(status_code=404, detail=f"File not found on disk: {file_path}")
        
        with open(file_path, "rb") as f:
            file_content = f.read()
        
        media_type = "application/octet-stream"
        if file_info["type"] == "RDF":
            if file_path.suffix.lower() == ".ttl":
                media_type = "text/turtle"
            elif file_path.suffix.lower() == ".rdf":
                media_type = "application/rdf+xml"
        elif file_info["type"] == "SHACL":
            media_type = "text/turtle"
        elif file_info["type"] == "UML":
            media_type = "image/png"
        
        return Response(
            content=file_content,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={file_info['name']}"}
        )
        
    except HTTPException as e:
        # Let HTTPException propagate as-is (404, etc)
        raise e
    except Exception as e:
        import logging
        logging.exception(f"Error serving file_id={file_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while downloading file: {str(e)}",
        )
