from pydantic import BaseModel
from typing import List, Optional

class RecipeBase(BaseModel):
    name: str
    cuisine: str
    is_vegetarian: bool
    prep_time_minutes: int
    ingredients: List[str]
    difficulty: str
    instructions: str
    tags: List[str]

class RecipeCreate(RecipeBase):
    pass

class RecipeResponse(RecipeBase):
    id: str

    class Config:
        from_attributes = True

class AISuggestionRequest(BaseModel):
    ingredients: List[str]

class AISimplifyRequest(BaseModel):
    instructions: str
