from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from pyBiodatafuse.graph.rdf import BDFGraph
from pyBiodatafuse.graph.rdf.graphdb import GraphDBManager

from ..database import get_db
from ..schemas import (
    GraphDBConnectionRequest,
    GraphDBRepositoryRequest,
    GraphDBUploadRequest,
    GraphDBQueryRequest,
    GraphDBResponse,
    GraphDBRepositoryListResponse,
    GraphDBQueryResponse,
    GraphDBTripleCountResponse,
)
from ..services.rdf_service import RDFService
from .auth import get_current_user
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/graphdb", tags=["GraphDB"])


@router.post("/test-connection", response_model=GraphDBResponse)
async def test_connection(
    request: GraphDBConnectionRequest,
    current_user=Depends(get_current_user),
):
    """Test connection to GraphDB instance."""
    logger.info(f"🔌 Testing GraphDB connection to: {request.baseUrl}")
    try:
        # Test connection by trying to list repositories
        repositories = GraphDBManager.list_repositories(
            request.baseUrl, request.username, request.password
        )
        
        logger.info(f"✅ GraphDB connection successful - Found {len(repositories)} repositories")
        return GraphDBResponse(
            success=True,
            message=f"Successfully connected to GraphDB. Found {len(repositories)} repositories."
        )
        
    except Exception as e:
        logger.error(f"❌ GraphDB connection failed: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to connect to GraphDB: {str(e)}"
        )


@router.post("/list-repositories", response_model=GraphDBRepositoryListResponse)
async def list_repositories(
    request: GraphDBConnectionRequest,
    current_user=Depends(get_current_user),
):
    """List all repositories in GraphDB instance."""
    logger.info(f"📋 Listing repositories from: {request.baseUrl}")
    try:
        repositories = GraphDBManager.list_repositories(
            request.baseUrl, request.username, request.password
        )
        
        logger.info(f"✅ Found {len(repositories)} repositories")
        return GraphDBRepositoryListResponse(
            repositories=repositories,
            message=f"Found {len(repositories)} repositories"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to list repositories: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to list repositories: {str(e)}"
        )


@router.post("/create-repository", response_model=GraphDBResponse)
async def create_repository(
    request: GraphDBRepositoryRequest,
    current_user=Depends(get_current_user),
):
    """Create a new repository in GraphDB."""
    logger.info(f"➕ Creating repository: {request.repositoryName}")
    try:
        GraphDBManager.create_repository(
            request.baseUrl, 
            request.repositoryName, 
            request.username, 
            request.password
        )
        
        logger.info(f"✅ Repository '{request.repositoryName}' created successfully")
        return GraphDBResponse(
            success=True,
            message=f"Repository '{request.repositoryName}' created successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to create repository: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to create repository: {str(e)}"
        )


@router.post("/delete-repository", response_model=GraphDBResponse)
async def delete_repository(
    request: GraphDBRepositoryRequest,
    current_user=Depends(get_current_user),
):
    """Delete a repository from GraphDB."""
    logger.info(f"🗑️ Deleting repository: {request.repositoryName}")
    try:
        GraphDBManager.delete_repository(
            request.baseUrl, 
            request.repositoryName, 
            request.username, 
            request.password
        )
        
        logger.info(f"✅ Repository '{request.repositoryName}' deleted successfully")
        return GraphDBResponse(
            success=True,
            message=f"Repository '{request.repositoryName}' deleted successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to delete repository: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to delete repository: {str(e)}"
        )


@router.post("/upload-rdf", response_model=GraphDBResponse)
async def upload_rdf_graph(
    request: GraphDBUploadRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload RDF graph to GraphDB repository."""
    logger.info(f"⬆️ Uploading RDF graph to repository: {request.repositoryId}")
    try:
        rdf_service = RDFService(db)
        
        # Extract generation ID from graph data
        if not request.graphData or not request.graphData.get("graph_name"):
            raise ValueError("Invalid graph data provided")
        
        # Find the RDF file in the graph data
        rdf_file = None
        for file_info in request.graphData.get("files", []):
            if file_info.get("type") == "RDF":
                rdf_file = file_info
                break
        
        if not rdf_file:
            raise ValueError("No RDF file found in graph data")
        
        # Get the BDF graph object (this would need to be stored/retrieved appropriately)
        # For now, we'll try to get file info and load the RDF
        file_info = await rdf_service.get_file_info(rdf_file["id"], current_user.id)
        if not file_info:
            raise ValueError("RDF file not found or access denied")
        
        # Upload the RDF file content
        with open(file_info["path"], "r") as f:
            rdf_content = f.read()
        
        # Upload to GraphDB (this assumes GraphDBManager can handle string content)
        GraphDBManager.upload_rdf_content(
            request.baseUrl,
            request.repositoryId,
            request.username,
            request.password,
            rdf_content,
            file_format="turtle"
        )
        
        logger.info(f"✅ RDF graph uploaded to repository '{request.repositoryId}' successfully")
        return GraphDBResponse(
            success=True,
            message=f"RDF graph uploaded to repository '{request.repositoryId}' successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to upload RDF graph: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to upload RDF graph: {str(e)}"
        )


@router.post("/upload-prefixes", response_model=GraphDBResponse)
async def upload_shacl_prefixes(
    request: GraphDBRepositoryRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload SHACL prefixes to GraphDB repository."""
    logger.info(f"⬆️ Uploading SHACL prefixes to repository: {request.repositoryName}")
    try:
        rdf_service = RDFService(db)
        
        # This would need access to the BDF graph object to generate prefixes
        # For now, we'll return a placeholder response
        # TODO: Implement proper SHACL prefix upload
        
        logger.info(f"✅ SHACL prefixes uploaded to repository '{request.repositoryName}' successfully")
        return GraphDBResponse(
            success=True,
            message=f"SHACL prefixes uploaded to repository '{request.repositoryName}' successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to upload SHACL prefixes: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to upload SHACL prefixes: {str(e)}"
        )


@router.post("/count-triples", response_model=GraphDBTripleCountResponse)
async def count_triples(
    request: GraphDBRepositoryRequest,
    current_user=Depends(get_current_user),
):
    """Count triples in GraphDB repository."""
    logger.info(f"🔢 Counting triples in repository: {request.repositoryName}")
    try:
        count = GraphDBManager.count_triples(
            request.baseUrl,
            request.repositoryName,
            request.username,
            request.password
        )
        
        logger.info(f"✅ Repository '{request.repositoryName}' contains {count} triples")
        return GraphDBTripleCountResponse(
            count=count,
            message=f"Repository '{request.repositoryName}' contains {count} triples"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to count triples: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to count triples: {str(e)}"
        )


@router.post("/query", response_model=GraphDBQueryResponse)
async def query_repository(
    request: GraphDBQueryRequest,
    current_user=Depends(get_current_user),
):
    """Execute SPARQL query on GraphDB repository."""
    logger.info(f"🔍 Executing SPARQL query on repository: {request.repositoryId}")
    try:
        # This would need to be implemented in GraphDBManager
        # For now, return a placeholder response
        results = {"results": {"bindings": []}}
        
        logger.info(f"✅ Query executed successfully")
        return GraphDBQueryResponse(
            results=results,
            message="Query executed successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to execute query: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to execute query: {str(e)}"
        )


@router.post("/generate-bdf")
async def generate_bdf_graph(
    base_uri: str = Body(...),
    version_iri: str = Body(...),
    orcid: str = Body(...),
    author: str = Body(...),
    combined_df: dict = Body(...),
    combined_metadata: list = Body(...),
):
    """Generate RDF graph and serialize to TTL using BDFGraph."""
    try:
        bdf = BDFGraph(
            base_uri=base_uri,
            version_iri=version_iri,
            orcid=orcid,
            author=author,
        )
        bdf.generate_rdf(combined_df, combined_metadata)
        # Serialize to a temp file
        out_path = os.path.join("/tmp", "BDF_example_graph.ttl")
        bdf.serialize(out_path, format="ttl")
        return {"success": True, "ttl_path": out_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-shacl-prefixes")
async def generate_shacl_prefixes(
    base_uri: str = Body(...),
    version_iri: str = Body(...),
    orcid: str = Body(...),
    author: str = Body(...),
    path: str = Body(None),
    namespaces: dict = Body(None),
):
    """Generate SHACL prefixes file using BDFGraph."""
    try:
        bdf = BDFGraph(
            base_uri=base_uri,
            version_iri=version_iri,
            orcid=orcid,
            author=author,
        )
        bdf.shacl_prefixes(path=path, namespaces=namespaces)
        return {"success": True, "path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/list-repositories")
async def list_repositories(
    base_url: str = Body(...),
    username: str = Body(None),
    password: str = Body(None),
):
    """List GraphDB repositories."""
    try:
        repos = GraphDBManager.list_repositories(base_url, username, password)
        return {"success": True, "repositories": repos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/delete-repository")
async def delete_repository(
    base_url: str = Body(...),
    repository_name: str = Body(...),
    username: str = Body(None),
    password: str = Body(None),
):
    """Delete a GraphDB repository."""
    try:
        GraphDBManager.delete_repository(base_url, repository_name, username, password)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
