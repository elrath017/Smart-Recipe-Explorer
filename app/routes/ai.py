from fastapi import APIRouter, HTTPException
from app.schemas import AISuggestionRequest, AISimplifyRequest
from app.services import ai_service

router = APIRouter()

@router.post("/suggest")
def suggest(request: AISuggestionRequest):
    if not request.ingredients:
        raise HTTPException(status_code=400, detail="Ingredients list cannot be empty")
    suggestion = ai_service.suggest_recipe(request.ingredients)
    if suggestion.startswith("AI Error:"):
        raise HTTPException(status_code=500, detail=suggestion)
    return {"suggestion": suggestion}

@router.post("/simplify")
def simplify(request: AISimplifyRequest):
    if not request.instructions.strip():
        raise HTTPException(status_code=400, detail="Instructions cannot be empty")
    simplified = ai_service.simplify_recipe(request.instructions)
    if simplified.startswith("AI Error:"):
        raise HTTPException(status_code=500, detail=simplified)
    return {"simplified_instructions": simplified}
