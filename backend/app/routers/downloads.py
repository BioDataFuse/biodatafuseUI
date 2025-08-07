from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..models import RDFGeneration
from .auth import get_current_user
import os
import tempfile
import zipfile
from typing import Optional
from sqlalchemy import select

router = APIRouter()

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

@router.get("/download-rdf/{generation_id}")
async def download_rdf_graph(
    generation_id: str, 
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Download the main RDF graph file"""
    generation = await get_generation_by_id(db, generation_id, current_user.id)
    
    # Find the main RDF file (usually .ttl or .rdf)
    rdf_file = None
    for file in generation.generated_files:
        file_name = file.get('name', '').lower()
        if file_name.endswith('.ttl') or file_name.endswith('.rdf'):
            if not ('shacl' in file_name or 'shex' in file_name or 'prefix' in file_name):
                rdf_file = file
                break
    
    if not rdf_file:
        raise HTTPException(status_code=404, detail="RDF graph file not found")
    
    file_path = rdf_file.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="RDF file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=rdf_file.get('name', 'graph.ttl'),
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
    
    # Find SHACL shapes file (not prefixes)
    shacl_file = None
    for file in generation.generated_files:
        file_name = file.get('name', '').lower()
        if 'shacl' in file_name and 'prefix' not in file_name and file_name.endswith('.ttl'):
            shacl_file = file
            break
    
    if not shacl_file:
        raise HTTPException(status_code=404, detail="SHACL shapes file not found")
    
    file_path = shacl_file.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="SHACL file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=shacl_file.get('name', 'shacl_shapes.ttl'),
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
    
    # Find SHACL prefixes file
    prefixes_file = None
    for file in generation.generated_files:
        file_name = file.get('name', '').lower()
        if 'shacl' in file_name and 'prefix' in file_name and file_name.endswith('.ttl'):
            prefixes_file = file
            break
    
    if not prefixes_file:
        raise HTTPException(status_code=404, detail="SHACL prefixes file not found")
    
    file_path = prefixes_file.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="SHACL prefixes file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=prefixes_file.get('name', 'shacl_prefixes.ttl'),
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
    shex_file = find_file_by_pattern(generation.generated_files, 'shex')
    if not shex_file:
        raise HTTPException(status_code=404, detail="ShEx shapes file not found")
    
    file_path = shex_file.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="ShEx file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=shex_file.get('name', 'shex_shapes.shex'),
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
    preview_file = None
    for file in generation.generated_files:
        file_name = file.get('name', '').lower()
        if 'shacl' in file_name and file_name.endswith('.png') and 'shex' not in file_name:
            preview_file = file
            break
    
    if not preview_file:
        raise HTTPException(status_code=404, detail="SHACL preview diagram not found")
    
    file_path = preview_file.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="SHACL preview file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=preview_file.get('name', 'shacl_diagram.png'),
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
    preview_file = None
    for file in generation.generated_files:
        file_name = file.get('name', '').lower()
        if 'shex' in file_name and file_name.endswith('.png'):
            preview_file = file
            break
    
    if not preview_file:
        raise HTTPException(status_code=404, detail="ShEx preview diagram not found")
    
    file_path = preview_file.get('path')
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="ShEx preview file not found on disk")
    
    return FileResponse(
        path=file_path,
        filename=preview_file.get('name', 'shex_diagram.png'),
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
    
    # Create a temporary ZIP file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_zip:
        with zipfile.ZipFile(temp_zip.name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in generation.generated_files:
                file_path = file.get('path')
                file_name = file.get('name')
                
                if file_path and file_name and os.path.exists(file_path):
                    zip_file.write(file_path, file_name)
        
        return FileResponse(
            path=temp_zip.name,
            filename=f"{generation.graph_name}_generated_files.zip",
            media_type='application/zip'
        )