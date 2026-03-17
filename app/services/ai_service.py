import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.config import settings

# Langchain expects the API key in the environment or passed directly
if settings.gemini_api_key:
    os.environ["GOOGLE_API_KEY"] = settings.gemini_api_key

def suggest_recipe(ingredients: list[str]) -> str:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        prompt = f"Suggest a recipe that uses the following ingredients: {', '.join(ingredients)}. Provide the recipe name, a full list of ingredients with measurements, and short cooking steps."
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"AI Error: {str(e)}"

def simplify_recipe(instructions: str) -> str:
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        prompt = f"Simplify the following recipe instructions so they are beginner-friendly and easy to read. Provide them in clear bullet points or short numbered steps:\n\n{instructions}"
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as e:
        return f"AI Error: {str(e)}"
