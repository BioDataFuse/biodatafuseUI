# Updated FastAPI router
from pydantic import BaseModel
from sqlalchemy import select
from pathlib import Path
import json

from fastapi import APIRouter, Depends, HTTPException, Path as FastAPIPath
from ..services.cytoscape_service import CytoscapeService
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/visualize&analysis", tags=["Visualization"])

class CytoscapeRequest(BaseModel):
    graph_name: str

@router.post("/cytoscape/{set_id}")
async def cytoscape_visualization(
    set_id: int,  
    req: CytoscapeRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Generate graph data and return it as JSON for client-side Cytoscape loading
    """
    try:
        from ..models import Annotation
        result = await db.execute(
            select(Annotation).where(Annotation.identifier_set_id == set_id)
        )
        annotation = result.scalar_one_or_none()

        if not annotation or not annotation.combined_df:
            raise HTTPException(status_code=404, detail="Processed annotation not found.")

        graph_dir = Path(f"./data/processed/{set_id}")
        cytoscape_service = CytoscapeService(db)
        
        # Generate graph data instead of loading directly
        result = await cytoscape_service.generate_graph_data(annotation, graph_dir, req.graph_name)

        if result["success"]:
            return {
                "message": "Graph data generated successfully",
                "graph_data": result["graph_data"],
                "graph_name": req.graph_name
            }
        else:
            raise HTTPException(status_code=500, detail=result["message"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
