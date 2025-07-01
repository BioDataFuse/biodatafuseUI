from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from ..services.analysis_service import AnalysisService
from ..models import Annotation
from .auth import get_current_user
import matplotlib.pyplot as plt
import io
import base64

router = APIRouter(prefix="/visualize&analysis", tags=["Analysis"])

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')

@router.get("/summary/{set_id}")
async def get_graph_summary(
    set_id: int,
    # current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):

    try:
        result = await db.execute(
            select(Annotation).where(Annotation.identifier_set_id == set_id)
        )
        annotation = result.scalar_one_or_none()

        if not annotation:
            raise HTTPException(status_code=404, detail="Processed annotation not found.")
        
        analysis_service = AnalysisService(db)
        summary, error = await analysis_service.get_graph_summary(annotation, Path(f"./data/processed/{set_id}"))
        if error:
            raise HTTPException(status_code=500, detail=error)
        else:
            return {"summary_html": summary["summary_html"]}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nodes/{set_id}")
async def get_node_counts(
    set_id: int,
    db: AsyncSession = Depends(get_db),
    # current_user=Depends(get_current_user)
    ):

    try:
        result = await db.execute(
            select(Annotation).where(Annotation.identifier_set_id == set_id)
        )
        
        annotation = result.scalar_one_or_none()

        if not annotation:
            raise HTTPException(status_code=404, detail="Processed annotation not found.")
        
        analysis_service = AnalysisService(db)
        fig, error = await analysis_service.plot_node_counts(annotation, Path(f"./data/processed/{set_id}"))
        if error:
            raise HTTPException(status_code=500, detail=error)
        else:
            return {"image": fig_to_base64(fig)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/edges/{set_id}")
async def get_edge_counts(
    set_id: int, 
    db: AsyncSession = Depends(get_db), 
    # current_user=Depends(get_current_user)
    ):

    try:
        result = await db.execute(
            select(Annotation).where(Annotation.identifier_set_id == set_id)
        )
        annotation = result.scalar_one_or_none()

        if not annotation:
            raise HTTPException(status_code=404, detail="Processed annotation not found.")
      
        analysis_service = AnalysisService(db)
        fig, error = await analysis_service.plot_edge_counts(annotation, Path(f"./data/processed/{set_id}"))
        if error:
            raise HTTPException(status_code=500, detail=error)
        else:
            return {"image": fig_to_base64(fig)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
