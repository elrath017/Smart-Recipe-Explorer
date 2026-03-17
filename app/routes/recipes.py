from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas import RecipeCreate, RecipeResponse
from app.database import get_db
from app.services import recipe_service

router = APIRouter()

@router.post("/", response_model=RecipeResponse, status_code=201)
def create_recipe(recipe: RecipeCreate, db: Session = Depends(get_db)):
    return recipe_service.create_recipe(db=db, recipe=recipe)

@router.get("/", response_model=List[RecipeResponse])
def get_recipes(db: Session = Depends(get_db)):
    return recipe_service.get_recipes(db=db)

@router.get("/search", response_model=List[RecipeResponse])
def search_recipes(
    name: Optional[str] = None,
    cuisine: Optional[str] = None,
    vegetarian: Optional[bool] = None,
    max_prep_time: Optional[int] = None,
    ingredient: Optional[str] = None,
    tag: Optional[str] = None,
    db: Session = Depends(get_db)
):
    recipes = recipe_service.search_recipes(db, name, cuisine, vegetarian, max_prep_time, ingredient, tag)
    return recipes

@router.get("/{recipe_id}", response_model=RecipeResponse)
def get_recipe(recipe_id: str, db: Session = Depends(get_db)):
    recipe = recipe_service.get_recipe_by_id(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
