from fastapi import FastAPI
from app.database import engine, Base
from app.routes import recipes, ai

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Recipe Explorer with AI Assistance", version="1.0.0")

app.include_router(recipes.router, prefix="/recipes", tags=["Recipes"])
app.include_router(ai.router, prefix="/ai", tags=["AI API"])

@app.get("/")
def root():
    return {"message": "Welcome to Smart Recipe Explorer API!"}
