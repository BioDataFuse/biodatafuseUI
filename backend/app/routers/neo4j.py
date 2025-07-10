from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..services.neo4j_service import Neo4jService

from ..database import get_db
from .auth import get_current_user

router = APIRouter(prefix="/visualize&analysis", tags=["Visualization"])

@router.post("/neo4j/{set_id}")
async def neo4j_visualization(
    set_id: int,
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:
        from ..models import Annotation
        result = await db.execute(
            select(Annotation).where(Annotation.identifier_set_id == set_id)
        )
        annotation = result.scalar_one_or_none()

        if not annotation or not annotation.combined_df:
            raise HTTPException(status_code=404, detail="Processed annotation not found.")

        graph_dir = Path(f"./data/processed/{set_id}")
        neo4j_service = Neo4jService(db)
        result = await neo4j_service.load_graph_into_neo4j(annotation, graph_dir)

        if result["success"]:
            return {"message": result["message"]}
        else:
            raise HTTPException(status_code=500, detail=result["message"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
