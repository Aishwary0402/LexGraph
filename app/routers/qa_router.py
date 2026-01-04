from fastapi import APIRouter
from pydantic import BaseModel
from app.services.unified_service import UnifiedPipeline

router = APIRouter()
pipeline = UnifiedPipeline()


class Query(BaseModel):
    question: str
    top_k: int = 5


@router.post("/ask")
def ask_question(q: Query):
    result = pipeline.process(q.question, q.top_k)

    return {
        "answer": result["answer"],
        "shap_explanation": result["shap_explanation"],
        "graph": result["graph"]
    }