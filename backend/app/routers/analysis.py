from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.database import get_db
from backend.app.services.analysis_service import AnalysisService
from backend.app.models import Annotation
from backend.app.routes.auth import get_current_user
from pathlib import Path
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
    current_user=Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    print(f"[summary] Received request for set_id: {set_id}")

    try:
        from backend.app.models import Annotation
        result = await db.execute(
            select(Annotation).where(Annotation.identifier_set_id == set_id)
        )
        annotation = result.scalar_one_or_none()

        if not annotation:
            raise HTTPException(status_code=404, detail="Processed annotation not found.")

        summary, error = AnalysisService.get_graph_summary(annotation, Path(f"./data/processed/{set_id}"))
        if error:
            raise HTTPException(status_code=500, detail=error)
        else:
            return summary

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/nodes/{set_id}")
async def get_node_counts(
    set_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
    ):
    print(f"[nodes] Received request for set_id: {set_id}")

    try:
        from backend.app.models import Annotation
        result = await db.execute(
            select(Annotation).where(Annotation.identifier_set_id == set_id)
        )
        annotation = result.scalar_one_or_none()

        if not annotation:
            raise HTTPException(status_code=404, detail="Processed annotation not found.")

        fig, error = AnalysisService.plot_node_counts(annotation, Path(f"./data/processed/{set_id}"))
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
    current_user=Depends(get_current_user)
    ):
    print(f"[edges] Received request for set_id: {set_id}")

    try:
        from backend.app.models import Annotation
        result = await db.execute(
            select(Annotation).where(Annotation.identifier_set_id == set_id)
        )
        annotation = result.scalar_one_or_none()

        if not annotation:
            raise HTTPException(status_code=404, detail="Processed annotation not found.")

        fig, error = AnalysisService.plot_edge_counts(annotation, Path(f"./data/processed/{set_id}"))
        if error:
            raise HTTPException(status_code=500, detail=error)
        else:
            return {"image": fig_to_base64(fig)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
