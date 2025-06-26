from pydantic import BaseModel
from sqlalchemy import select
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Path as FastAPIPath
from backend.app.services.cytoscape_service import CytoscapeService
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
    print(f"[Cytoscape] Received request for set_id: {set_id}")

    try:
        from backend.app.models import Annotation
        result = await db.execute(
            select(Annotation).where(Annotation.identifier_set_id == set_id)
        )
        annotation = result.scalar_one_or_none()

        if not annotation or not annotation.combined_df:
            raise HTTPException(status_code=404, detail="Processed annotation not found.")

        graph_dir = Path(f"./data/processed/{set_id}")
        cytoscape_service = CytoscapeService(db)
        result = await cytoscape_service.load_graph_into_cytoscape(annotation, graph_dir, req.graph_name)

        if result["success"]:
            return {"message": result["message"]}
        else:
            raise HTTPException(status_code=500, detail=result["message"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
