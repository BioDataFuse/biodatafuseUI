# backend/app/api/routes/analysis.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.graph_analysis_service import GraphAnalysisService

router = APIRouter(prefix="/analysis", tags=["Analysis"])

class ChemicalInput(BaseModel):
    chemicals: str

@router.post("/patent-data/")
async def analyze_patents(input_data: ChemicalInput):
    try:
        chemical_list = [c.strip() for c in input_data.chemicals.strip().split('\n') if c.strip()]
        if not chemical_list:
            raise HTTPException(status_code=400, detail="No valid chemicals provided.")
        
        analysis_service = GraphAnalysisService()
        result_df = await analysis_service.run_patent_analysis(chemical_list)

        # Group entries by CID and return summaries
        summary = {}
        for cid in result_df.index.unique():
            subset = result_df.loc[[cid]] if isinstance(result_df.loc[cid], pd.Series) else result_df.loc[cid]
            summary[cid] = subset.to_dict(orient="records")

        return {"success": True, "summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
