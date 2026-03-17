from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_recipes.db"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_create_recipe():
    response = client.post(
        "/recipes/",
        json={
            "name": "Paneer Butter Masala",
            "cuisine": "Indian",
            "is_vegetarian": True,
            "prep_time_minutes": 40,
            "ingredients": ["paneer", "tomato", "cream", "butter"],
            "difficulty": "medium",
            "instructions": "Cook tomatoes, add paneer, simmer with cream.",
            "tags": ["dinner", "rich"]
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Paneer Butter Masala"

def test_get_recipes():
    client.post(
        "/recipes/",
        json={
            "name": "Quick Salad",
            "cuisine": "Global",
            "is_vegetarian": True,
            "prep_time_minutes": 10,
            "ingredients": ["lettuce", "tomato", "cucumber"],
            "difficulty": "easy",
            "instructions": "Chop and mix.",
            "tags": ["healthy"]
        }
    )
    response = client.get("/recipes/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_search_recipes():
    client.post(
        "/recipes/",
        json={
            "name": "Quick Salad",
            "cuisine": "Global",
            "is_vegetarian": True,
            "prep_time_minutes": 10,
            "ingredients": ["lettuce", "tomato", "cucumber"],
            "difficulty": "easy",
            "instructions": "Chop and mix.",
            "tags": ["healthy"]
        }
    )
    response = client.get("/recipes/search?cuisine=Global&vegetarian=true")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == "Quick Salad"

def test_ai_suggest_empty():
    response = client.post("/ai/suggest", json={"ingredients": []})
    assert response.status_code == 400
