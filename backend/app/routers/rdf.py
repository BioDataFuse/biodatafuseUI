from typing import Dict, List, Optional
import os
import tempfile
import uuid
import zipfile
from pathlib import Path
import logging

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..database import get_db
from ..schemas import RDFGenerationRequest, RDFGenerationResponse
from ..services.rdf_service import RDFService
from .auth import get_current_user
from ..models import RDFGeneration

router = APIRouter(prefix="/rdf", tags=["RDF Generation"])

logger = logging.getLogger("rdf_router")


async def get_generation_by_id(db: AsyncSession, generation_id: str, user_id: int):
    """Get RDF generation record by ID for the current user"""
    result = await db.execute(
        select(RDFGeneration).where(
            RDFGeneration.generation_id == generation_id,
            RDFGeneration.user_id == user_id
        )
    )
    generation = result.scalar_one_or_none()
    
    if not generation:
        raise HTTPException(status_code=404, detail="Generation not found")
    return generation

def find_file_by_pattern(generated_files: list, pattern: str) -> Optional[dict]:
    """Find a file in generated_files that matches a pattern"""
    for file in generated_files:
        if pattern in file.get('name', '').lower():
            return file
    return None


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
        generation_id = str(uuid.uuid4())
        
        # Generate the main RDF graph using the service
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
            custom_namespaces=request.custom_namespaces if hasattr(request, 'custom_namespaces') else None,
        )
        
        # Extract generated files from the result
        generated_files = []
        if hasattr(result, 'generated_files'):
            generated_files = [
                {
                    "id": file.id,
                    "name": file.name,
                    "type": file.type,
                    "size": file.size,
                    "path": None  # Don't expose paths in API response
                }
                for file in result.generated_files
            ]
        
        # Store generation in database
        rdf_generation = RDFGeneration(
            generation_id=generation_id,
            identifier_set_id=request.identifier_set_id,
            graph_name=request.graph_name,
            base_uri=request.base_uri,
            version_iri=request.version_iri,
            author_name=request.author_name,
            author_email=request.author_email,
            orcid=request.orcid,
            generate_shacl=request.generate_shacl,
            shacl_threshold=request.shacl_threshold,
            generate_uml_diagram=request.generate_uml_diagram,
            generate_shex=request.generate_shex,
            shex_threshold=request.shex_threshold,
            generated_files=generated_files,
            status="completed",
            user_id=current_user.id
        )
        
        db.add(rdf_generation)
        await db.commit()
        await db.refresh(rdf_generation)
        
        response_result = {
            "generation_id": generation_id,
            "graph_name": request.graph_name,
            "generated_files": generated_files,
            "message": "RDF graph generated successfully",
            "status": "completed"
        }
        
        logger.info(f"✅ RDF generation completed successfully")
        return response_result
        
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


# Specific download endpoints by generation ID
@router.get("/download-rdf/{generation_id}")
async def download_rdf_graph(
    generation_id: str, 
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download the main RDF graph file"""
    generation = await get_generation_by_id(db, generation_id, current_user.id)
    
    # Find the main RDF file by looking up the file ID in the RDF files table
    rdf_file_info = None
    for file in generation.generated_files:
        if file.get('type') == 'RDF':
            # Get the actual file info from the RDF service
            rdf_service = RDFService(db)
            rdf_file_info = await rdf_service.get_file_info(file.get('id'), current_user.id)
            break
    
    if not rdf_file_info:
        raise HTTPException(status_code=404, detail="RDF graph file not found")
    
    file_path = rdf_file_info.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="RDF file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=rdf_file_info.get('name', 'graph.ttl'),
        media_type='text/turtle'
    )


@router.get("/download-shacl/{generation_id}")
async def download_shacl_shapes(
    generation_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download SHACL shapes file"""
    generation = await get_generation_by_id(db, generation_id, current_user.id)
    
    # Find SHACL shapes file
    shacl_file_info = None
    for file in generation.generated_files:
        if file.get('type') == 'SHACL':
            rdf_service = RDFService(db)
            shacl_file_info = await rdf_service.get_file_info(file.get('id'), current_user.id)
            break
    
    if not shacl_file_info:
        raise HTTPException(status_code=404, detail="SHACL shapes file not found")
    
    file_path = shacl_file_info.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="SHACL file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=shacl_file_info.get('name', 'shacl_shapes.ttl'),
        media_type='text/turtle'
    )


@router.get("/download-shacl-prefixes/{generation_id}")
async def download_shacl_prefixes(
    generation_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download SHACL prefixes file"""
    generation = await get_generation_by_id(db, generation_id, current_user.id)
    
    # Find SHACL prefixes file - look for files with "SHACL_Prefixes" type
    prefixes_file_info = None
    for file in generation.generated_files:
        if file.get('type') == 'SHACL_Prefixes' or ('prefix' in file.get('name', '').lower() and 'shacl' in file.get('name', '').lower()):
            rdf_service = RDFService(db)
            prefixes_file_info = await rdf_service.get_file_info(file.get('id'), current_user.id)
            break
    
    if not prefixes_file_info:
        raise HTTPException(status_code=404, detail="SHACL prefixes file not found")
    
    file_path = prefixes_file_info.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="SHACL prefixes file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=prefixes_file_info.get('name', 'shacl_prefixes.ttl'),
        media_type='text/turtle'
    )


@router.get("/download-shex/{generation_id}")
async def download_shex_shapes(
    generation_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download ShEx shapes file"""
    generation = await get_generation_by_id(db, generation_id, current_user.id)
    
    # Find ShEx shapes file
    shex_file_info = None
    for file in generation.generated_files:
        if file.get('type') == 'ShEx':
            rdf_service = RDFService(db)
            shex_file_info = await rdf_service.get_file_info(file.get('id'), current_user.id)
            break
    
    if not shex_file_info:
        raise HTTPException(status_code=404, detail="ShEx shapes file not found")
    
    file_path = shex_file_info.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="ShEx file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=shex_file_info.get('name', 'shex_shapes.shex'),
        media_type='application/octet-stream'
    )


@router.get("/download-shacl-preview/{generation_id}")
async def download_shacl_preview(
    generation_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download SHACL UML diagram preview"""
    generation = await get_generation_by_id(db, generation_id, current_user.id)
    
    # Find SHACL UML diagram file
    preview_file_info = None
    for file in generation.generated_files:
        if file.get('type') == 'UML' and 'shacl' in file.get('name', '').lower():
            rdf_service = RDFService(db)
            preview_file_info = await rdf_service.get_file_info(file.get('id'), current_user.id)
            break
    
    if not preview_file_info:
        raise HTTPException(status_code=404, detail="SHACL preview diagram not found")
    
    file_path = preview_file_info.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="SHACL preview file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=preview_file_info.get('name', 'shacl_diagram.png'),
        media_type='image/png'
    )


@router.get("/download-shex-preview/{generation_id}")
async def download_shex_preview(
    generation_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download ShEx UML diagram preview"""
    generation = await get_generation_by_id(db, generation_id, current_user.id)
    
    # Find ShEx UML diagram file
    preview_file_info = None
    for file in generation.generated_files:
        if file.get('type') in ['ShEx_UML', 'UML'] and 'shex' in file.get('name', '').lower():
            rdf_service = RDFService(db)
            preview_file_info = await rdf_service.get_file_info(file.get('id'), current_user.id)
            break
    
    if not preview_file_info:
        raise HTTPException(status_code=404, detail="ShEx preview diagram not found")
    
    file_path = preview_file_info.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="ShEx preview file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=preview_file_info.get('name', 'shex_diagram.png'),
        media_type='image/png'
    )


@router.get("/download-all/{generation_id}")
async def download_all_files(
    generation_id: str,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download all generated files as a ZIP archive"""
    generation = await get_generation_by_id(db, generation_id, current_user.id)
    
    if not generation.generated_files:
        raise HTTPException(status_code=404, detail="No generated files found")
    
    rdf_service = RDFService(db)
    
    # Create a temporary ZIP file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in generation.generated_files:
                # Get actual file info from the RDF service
                file_info = await rdf_service.get_file_info(file.get('id'), current_user.id)
                if file_info and os.path.exists(file_info['path']):
                    zip_file.write(file_info['path'], file_info['name'])
        
        return FileResponse(
            path=temp_zip.name,
            filename=f"{generation.graph_name}_generated_files.zip",
            media_type='application/zip'
        )
