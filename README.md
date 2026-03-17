# Smart Recipe Explorer with AI Assistance

## Project Overview
Smart Recipe Explorer is a full-stack web application designed to help users manage their recipes, search with various filters, and utilize Generative AI (Google Gemini) to suggest new recipes based on available ingredients or simplify complex recipe instructions.

## Features
- **Recipe Management:** Create and store recipes. Form fields clear automatically upon successful creation!
- **Advanced Search:** Filter by recipe name, cuisine, vegetarian preference, max prep time, ingredients, and tags.
- **List All:** View your entire recipe database with a single click.
- **AI Recipe Suggestion:** Input a list of ingredients and let AI generate a recipe for you!
- **AI Simplification:** Chain AI outputs natively in the UI to turn your generated complex procedures into simple, beginner-friendly bullet points.
- **RESTful API:** Robust FastAPI backend backing the application.
- **Modern UI:** Built with Streamlit for a fast and clean user experience.

## Tech Stack
- **Backend Framework:** FastAPI & Uvicorn
- **Frontend:** Streamlit
- **AI Service:** LangChain & Google Gemini 2.5 Flash API (`langchain-google-genai`)
- **Database:** SQLite with SQLAlchemy ORM
- **Environment Management:** `python-dotenv`
- **Testing:** `pytest` and FastAPI `TestClient`

## Project Structure
```text
smart_recipe_explorer/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── config.py
│   ├── routes/
│   │   ├── recipes.py
│   │   └── ai.py
│   └── services/
│       ├── recipe_service.py
│       └── ai_service.py
├── frontend/
│   └── streamlit_app.py
├── tests/
│   └── test_api.py
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Clone the repository and navigate to the project directory
```bash
git clone https://github.com/elrath017/Smart-Recipe-Explorer.git
cd Smart-Recipe-Explorer
```

### 2. Create a Virtual Environment (Optional but recommended)
```bash
python -m venv myenv
# On Windows:
myenv\Scripts\activate
# On macOS/Linux:
source myenv/bin/activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Environment Variables Setup
Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Edit the `.env` file and add your valid Gemini API Key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

---

## How to Run

### Run Backend
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```
The API will be available at: http://127.0.0.1:8000
Swagger Documentation: http://127.0.0.1:8000/docs

### Run Frontend
In a new terminal window, start the Streamlit UI:
```bash
streamlit run frontend/streamlit_app.py
```
The app will open in your browser automatically (usually http://localhost:8501).

---

## API Endpoint Documentation

### Recipes API
- `POST /recipes/` - Create a new recipe.
- `GET /recipes/` - Get a list of all recipes.
- `GET /recipes/search` - Search recipes with filters (`cuisine`, `vegetarian`, `max_prep_time`, `ingredient`, `tag`).
- `GET /recipes/{recipe_id}` - Get recipe details by ID.

### AI API
- `POST /ai/suggest` - Suggest a recipe from ingredients.
- `POST /ai/simplify` - Simplify a recipe.

## Example API Requests

### 1. Create Recipe
```bash
curl -X 'POST' \
  'http://localhost:8000/recipes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Paneer Butter Masala",
  "cuisine": "Indian",
  "is_vegetarian": true,
  "prep_time_minutes": 40,
  "ingredients": ["paneer","tomato","cream","butter"],
  "difficulty": "medium",
  "instructions": "Cook tomatoes, add paneer, simmer with cream.",
  "tags": ["dinner","rich"]
}'
```

### 2. Suggest Recipe (AI)
```bash
curl -X 'POST' \
  'http://localhost:8000/ai/suggest' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "ingredients": ["paneer", "onion", "tomato"]
}'
```

## Example Screenshots
*(You can add screenshots here for the frontend UI after you run the application)*
