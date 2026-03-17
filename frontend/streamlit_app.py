import streamlit as st
import requests

API_BASE_URL = "http://localhost:8000"

st.set_page_config(page_title="Smart Recipe Explorer", layout="wide")
st.title("Smart Recipe Explorer with AI Assistance 🍳")

# Navigation
page = st.sidebar.selectbox("Navigate", ["Browse Recipes", "Add Recipe", "AI Assistant"])

if page == "Browse Recipes":
    st.header("Search & Filter Recipes")
    
    # Add an explicit Recipe Name keyword search
    name_search = st.text_input("🔍 Search by Recipe Name")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        cuisine = st.text_input("Cuisine")
    with col2:
        max_prep = st.number_input("Max Prep Time (mins)", min_value=0, value=0)
    with col3:
        veg_only = st.checkbox("Vegetarian Only")
    with col4:
        ingredient_search = st.text_input("Contains Ingredient")

    btn_col1, btn_col2 = st.columns([1, 10])
    with btn_col1:
        search_clicked = st.button("Search")
    with btn_col2:
        list_all_clicked = st.button("List All Recipes")

    if search_clicked or list_all_clicked:
        try:
            if list_all_clicked:
                # If List All is clicked, simply call the get all recipes endpoint
                response = requests.get(f"{API_BASE_URL}/recipes/")
            else:
                params = {}
                if name_search:
                    params['name'] = name_search
                if cuisine:
                    params['cuisine'] = cuisine
                if veg_only:
                    params['vegetarian'] = True
                if max_prep > 0:
                    params['max_prep_time'] = max_prep
                if ingredient_search:
                    params['ingredient'] = ingredient_search
                
                response = requests.get(f"{API_BASE_URL}/recipes/search", params=params)

            if response.status_code == 200:
                recipes = response.json()
                if not recipes:
                    if list_all_clicked:
                        st.warning("No recipes found in the database. Add some first!")
                    else:
                        st.warning("No recipes found matching your criteria.")
                for r in recipes:
                    with st.expander(f"{r['name']} ({r.get('cuisine', 'N/A')}) - {r.get('prep_time_minutes', 0)} mins"):
                        st.write(f"**Difficulty:** {r.get('difficulty', 'N/A')}")
                        st.write(f"**Vegetarian:** {'Yes' if r.get('is_vegetarian') else 'No'}")
                        if 'tags' in r and isinstance(r['tags'], list):
                            st.write(f"**Tags:** {', '.join(r['tags'])}")
                        if 'ingredients' in r and isinstance(r['ingredients'], list):
                            st.write("**Ingredients:**")
                            st.write(", ".join(r['ingredients']))
                        st.write("**Instructions:**")
                        st.write(r.get('instructions', ''))
            else:
                st.error("Error fetching recipes.")
        except Exception as e:
            st.error(f"Could not connect to API: {e}. Is the backend running?")

elif page == "Add Recipe":
    st.header("Add a New Recipe")
    
    if "recipe_saved_success" in st.session_state and st.session_state.recipe_saved_success:
        st.success("Recipe added successfully!")
        st.session_state.recipe_saved_success = False

    with st.form("add_recipe_form"):
        name = st.text_input("Recipe Name", key="add_name")
        cuisine = st.text_input("Cuisine", key="add_cuisine")
        is_veg = st.checkbox("Is Vegetarian?", key="add_is_veg")
        prep_time = st.number_input("Prep Time (minutes)", min_value=1, value=30, key="add_prep")
        ingredients_input = st.text_area("Ingredients (comma-separated)", key="add_ing")
        difficulty = st.selectbox("Difficulty", ["easy", "medium", "hard"], key="add_diff")
        instructions = st.text_area("Instructions", key="add_inst")
        tags_input = st.text_input("Tags (comma-separated)", key="add_tags")
        
        submitted = st.form_submit_button("Save Recipe")
        
        if submitted:
            if not name or not cuisine or not ingredients_input or not instructions:
                st.error("Please fill in all required fields: Recipe Name, Cuisine, Ingredients, and Instructions.")
            else:
                payload = {
                    "name": name,
                    "cuisine": cuisine,
                    "is_vegetarian": is_veg,
                    "prep_time_minutes": prep_time,
                    "ingredients": [i.strip() for i in ingredients_input.split(",") if i.strip()],
                    "difficulty": difficulty,
                    "instructions": instructions,
                    "tags": [t.strip() for t in tags_input.split(",") if t.strip()]
                }
                try:
                    res = requests.post(f"{API_BASE_URL}/recipes/", json=payload)
                    if res.status_code == 201:
                        st.session_state.recipe_saved_success = True
                        
                        # Clear specific widget keys from session_state
                        keys_to_clear = ["add_name", "add_cuisine", "add_is_veg", "add_prep", "add_ing", "add_diff", "add_inst", "add_tags"]
                        for k in keys_to_clear:
                            if k in st.session_state:
                                del st.session_state[k]
                                
                        st.rerun()
                    else:
                        st.error(f"Failed to add recipe: {res.text}")
                except Exception as e:
                    st.error(f"Could not connect to API: {e}. Is the backend running?")

elif page == "AI Assistant":
    st.header("AI Assistant 🤖")
    
    if "generated_recipe" not in st.session_state:
        st.session_state.generated_recipe = None
        
    if "simplified_recipe" not in st.session_state:
        st.session_state.simplified_recipe = None
    
    st.subheader("Suggest a Recipe from Ingredients")
    ingredients_list = st.text_area("What's in your fridge? (comma-separated ingredients)")
    
    # We use a standard button for generating
    if st.button("Generate Recipe with AI"):
        st.session_state.simplified_recipe = None  # Clear previous simplifications
        if ingredients_list:
            items = [i.strip() for i in ingredients_list.split(",") if i.strip()]
            with st.spinner("Generating recipe..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/ai/suggest", json={"ingredients": items})
                    if res.status_code == 200:
                        st.session_state.generated_recipe = res.json().get("suggestion", "")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Could not connect to API: {e}")
        else:
            st.warning("Please enter some ingredients.")

    # Always render the generated output if it exists in session state
    if st.session_state.generated_recipe:
        st.markdown("### Generated Recipe:")
        st.write(st.session_state.generated_recipe)
        
        # Display the simplify button below the generated recipe
        if st.button("Simplify Instructions"):
            with st.spinner("Simplifying..."):
                try:
                    res = requests.post(f"{API_BASE_URL}/ai/simplify", json={"instructions": st.session_state.generated_recipe})
                    if res.status_code == 200:
                        st.session_state.simplified_recipe = res.json().get("simplified_instructions", "")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Could not connect to API: {e}")

    # Render the simplified output if it exists in session state
    if st.session_state.simplified_recipe:
        st.markdown("---")
        st.markdown("### Simplified Version:")
        st.write(st.session_state.simplified_recipe)
