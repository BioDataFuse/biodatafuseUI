from pydantic import BaseModel
from sqlalchemy import select
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from ..services.cytoscape_service import CytoscapeService
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/visualize&analysis", tags=["Visualization"])

class CytoscapeRequest(BaseModel):
    graph_name: str

@router.post("/cytoscape/{set_id}")
async def get_cytoscape_graph_data(
    set_id: int,
    req: CytoscapeRequest,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieves a graph in Cytoscape JSON format.
    This data is intended to be consumed by a local application that interacts with Cytoscape.
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
        cytoscape_json_data, error = await cytoscape_service.get_cytoscape_json(
            annotation, graph_dir
        )

        if error:
            raise HTTPException(status_code=500, detail=error)

        return {
            "graph_data": cytoscape_json_data,
            "network_name": req.graph_name
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")