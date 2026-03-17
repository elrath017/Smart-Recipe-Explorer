from sqlalchemy.orm import Session
from app.models import Recipe
from app.schemas import RecipeCreate

def create_recipe(db: Session, recipe: RecipeCreate):
    db_recipe = Recipe(**recipe.model_dump())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_recipes(db: Session):
    return db.query(Recipe).all()

def get_recipe_by_id(db: Session, recipe_id: str):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()

def search_recipes(db: Session, name: str = None, cuisine: str = None, vegetarian: bool = None, max_prep_time: int = None, ingredient: str = None, tag: str = None):
    query = db.query(Recipe)
    
    if name is not None:
        query = query.filter(Recipe.name.ilike(f"%{name}%"))
    if cuisine is not None:
        query = query.filter(Recipe.cuisine.ilike(f"%{cuisine}%"))
    if vegetarian is not None:
        query = query.filter(Recipe.is_vegetarian == vegetarian)
    if max_prep_time is not None:
        query = query.filter(Recipe.prep_time_minutes <= max_prep_time)
        
    recipes = query.all()
    
    filtered_recipes = []
    for r in recipes:
        if ingredient and not any(ingredient.lower() in ing.lower() for ing in r.ingredients):
            continue
        if tag and not any(tag.lower() in t.lower() for t in r.tags):
            continue
        filtered_recipes.append(r)
        
    return filtered_recipes
