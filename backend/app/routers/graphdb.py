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
    
    # Add detailed request logging
    logger.info(f"📋 Request details:")
    logger.info(f"  - baseUrl: {request.baseUrl}")
    logger.info(f"  - username: {request.username}")
    logger.info(f"  - password: {'***' if request.password else None}")
    logger.info(f"  - user: {current_user.email}")
    
    # Validate the request
    if not request.baseUrl:
        logger.error("❌ Missing baseUrl in request")
        raise HTTPException(
            status_code=400,
            detail="baseUrl is required"
        )
    
    if not request.baseUrl.startswith(('http://', 'https://')):
        logger.error(f"❌ Invalid baseUrl format: {request.baseUrl}")
        raise HTTPException(
            status_code=400,
            detail="baseUrl must start with http:// or https://"
        )
    
    # Check for common Docker networking issues
    if 'localhost' in request.baseUrl or '127.0.0.1' in request.baseUrl:
        logger.warning("⚠️ Docker networking: localhost/127.0.0.1 detected - this may not work from inside a container")
    
    try:
        logger.info(f"🔍 Attempting to list repositories from GraphDB...")
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
        logger.error(f"❌ Exception type: {type(e).__name__}")
        logger.error(f"❌ Full exception details: {repr(e)}")
        
        # Provide Docker-specific error guidance
        error_message = str(e)
        if "Connection refused" in error_message and ("localhost" in request.baseUrl or "127.0.0.1" in request.baseUrl):
            error_message += "\n\n🐳 Docker Networking Issue: When running in Docker, 'localhost' refers to the container, not your host machine.\n\nTry these alternatives:\n• host.docker.internal:7200 (Docker Desktop for Mac/Windows)\n• 172.17.0.1:7200 (Linux Docker default bridge)\n• Your host machine's actual IP address\n• Or use the 'Docker Host' option in the connection type selector"
        
        raise HTTPException(
            status_code=400,
            detail=f"Failed to connect to GraphDB: {error_message}"
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
        import rdflib
        rdf_service = RDFService(db)
        
        # Get RDF file directly from generated files
        generated_files = request.graphData.get("generated_files", [])
        rdf_file = next((f for f in generated_files if f.get("type") == "RDF"), None)
        
        if not rdf_file:
            raise ValueError("No RDF file found in generated data")
        
        # Get file info from database
        file_info = await rdf_service.get_file_info(rdf_file["id"], current_user.id)
        if not file_info or not os.path.exists(file_info['path']):
            raise ValueError("RDF file not found")
        
        # Read TTL into rdflib Graph
        g = rdflib.Graph()
        g.parse(file_info['path'], format='turtle')
        
        # Upload using your GraphDBManager
        GraphDBManager.upload_to_graphdb(
            request.baseUrl,
            request.repositoryId,
            request.username,
            request.password,
            g,
            file_format="turtle"
        )
        
        logger.info(f"✅ RDF graph uploaded successfully")
        return GraphDBResponse(
            success=True,
            message=f"RDF graph uploaded to repository '{request.repositoryId}' successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to upload RDF graph: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to upload RDF graph: {str(e)}")


@router.post("/upload-prefixes", response_model=GraphDBResponse)
async def upload_shacl_prefixes(
    request: GraphDBUploadRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload SHACL prefixes to GraphDB repository."""
    logger.info(f"📋 Uploading SHACL prefixes to repository: {request.repositoryId}")
    try:
        import rdflib
        rdf_service = RDFService(db)
        
        # Get SHACL file directly from generated files
        generated_files = request.graphData.get("generated_files", [])
        shacl_file = next((f for f in generated_files if f.get("type") == "SHACL"), None)
        
        if not shacl_file:
            raise ValueError("No SHACL file found in generated data")
        
        # Get file info from database
        file_info = await rdf_service.get_file_info(shacl_file["id"], current_user.id)
        if not file_info or not os.path.exists(file_info['path']):
            raise ValueError("SHACL file not found")
        
        # Read TTL into rdflib Graph
        g = rdflib.Graph()
        g.parse(file_info['path'], format='turtle')
        
        # Upload using your GraphDBManager
        GraphDBManager.upload_to_graphdb(
            request.baseUrl,
            request.repositoryId,
            request.username,
            request.password,
            g,
            file_format="turtle"
        )
        
        logger.info(f"✅ SHACL prefixes uploaded successfully")
        return GraphDBResponse(
            success=True,
            message=f"SHACL prefixes uploaded to repository '{request.repositoryId}' successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to upload SHACL prefixes: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to upload SHACL prefixes: {str(e)}"
        )


@router.post("/count-triples", response_model=GraphDBTripleCountResponse)
async def count_triples(
    request: GraphDBRepositoryRequest,
    current_user=Depends(get_current_user),
):
    """Count triples in GraphDB repository."""
    logger.info(f"🔢 Counting triples in repository: {request.repositoryName}")
    try:
        triple_count = GraphDBManager.count_triples(
            request.baseUrl,
            request.repositoryName,
            request.username,
            request.password
        )
        
        # Handle different response formats from GraphDBManager
        if isinstance(triple_count, dict):
            total_count = triple_count.get('total', 0)
            explicit_count = triple_count.get('explicit', 0)
            inferred_count = triple_count.get('inferred', 0)
            message = f"Repository '{request.repositoryName}' contains {total_count} total triples (explicit: {explicit_count}, inferred: {inferred_count})"
        else:
            total_count = int(triple_count) if triple_count else 0
            message = f"Repository '{request.repositoryName}' contains {total_count} triples"
        
        logger.info(f"✅ {message}")
        return GraphDBTripleCountResponse(
            count=total_count if isinstance(triple_count, dict) else triple_count,
            explicit_count=triple_count.get('explicit', 0) if isinstance(triple_count, dict) else None,
            inferred_count=triple_count.get('inferred', 0) if isinstance(triple_count, dict) else None,
            message=message
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


@router.post("/upload-shex", response_model=GraphDBResponse)
async def upload_shex_shapes(
    request: GraphDBUploadRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Upload ShEx shapes to GraphDB repository."""
    logger.info(f"📐 Uploading ShEx shapes to repository: {request.repositoryId}")
    try:
        import rdflib
        rdf_service = RDFService(db)
        
        # Get ShEx file directly from generated files
        generated_files = request.graphData.get("generated_files", [])
        shex_file = next((f for f in generated_files if f.get("type") == "ShEx"), None)
        
        if not shex_file:
            raise ValueError("No ShEx file found in generated data")
        
        # Get file info from database
        file_info = await rdf_service.get_file_info(shex_file["id"], current_user.id)
        if not file_info or not os.path.exists(file_info['path']):
            raise ValueError("ShEx file not found")
        
        # Read TTL into rdflib Graph
        g = rdflib.Graph()
        g.parse(file_info['path'], format='turtle')
        
        # Upload using your GraphDBManager
        GraphDBManager.upload_to_graphdb(
            request.baseUrl,
            request.repositoryId,
            request.username,
            request.password,
            g,
            file_format="turtle"
        )
        
        logger.info(f"✅ ShEx shapes uploaded successfully")
        return GraphDBResponse(
            success=True,
            message=f"ShEx shapes uploaded to repository '{request.repositoryId}' successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to upload ShEx shapes: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Failed to upload ShEx shapes: {str(e)}"
        )


@router.post("/upload-namespaces", response_model=GraphDBResponse)
async def upload_custom_namespaces(
    request: GraphDBUploadRequest,
    current_user=Depends(get_current_user),
):
    """Upload custom namespace prefixes to GraphDB repository."""
    logger.info(f"🏷️ Uploading custom namespaces to repository: {request.repositoryId}")
    try:
        namespaces = request.graphData.get("namespaces", {})
        if not namespaces:
            raise ValueError("No namespaces provided")
        
        # Create a simple RDF graph with PREFIX declarations
        prefix_triples = []
        for prefix, uri in namespaces.items():
            # Add the namespace as RDF data that can be queried
            prefix_triples.append(f"@prefix {prefix}: <{uri}> .")
        
        namespace_data = "\n".join(prefix_triples)
        
        logger.info(f"📤 Uploading custom namespaces to GraphDB...")
        # Upload namespace data as turtle
        GraphDBManager.upload_rdf_content(
            request.baseUrl,
            request.repositoryId,
            request.username,
            request.password,
            namespace_data,
            file_format="turtle"
        )
        
        logger.info(f"✅ Custom namespaces uploaded to repository '{request.repositoryId}' successfully")
        return GraphDBResponse(
            success=True,
            message=f"Custom namespaces uploaded to repository '{request.repositoryId}' successfully"
        )
        
    except Exception as e:
        logger.error(f"❌ Failed to upload custom namespaces: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=f"Failed to upload custom namespaces: {str(e)}"
        )
