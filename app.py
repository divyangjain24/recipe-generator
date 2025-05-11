import streamlit as st
import requests

# --- Constants ---
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = st.secrets["API"]  # Securely loaded from Streamlit secrets

# --- Streamlit Page Config ---
st.set_page_config(page_title="AI Recipe Generator", page_icon="🍳", layout="centered")

# --- Session State Init ---
if "generated_recipe" not in st.session_state:
    st.session_state.generated_recipe = ""
if "current_recipe_name" not in st.session_state:
    st.session_state.current_recipe_name = ""

# --- Custom CSS ---
st.markdown("""
<style>
body, .stApp {
    background-color: #121212;
    color: #f5f5f5;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    background: linear-gradient(90deg, #ff6a00, #ee0979);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.stTextInput > div > div > input {
    background-color: #1e1e1e !important;
    color: white !important;
}
.recipe-box {
    background-color: #1f1f1f;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #333;
    box-shadow: 2px 2px 10px rgba(255,255,255,0.05);
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- Title ---
st.title("🍲 AI Recipe Generator")
st.subheader("Type any dish name and get a delicious recipe!")

# --- Input ---
recipe_name = st.text_input("Enter Recipe Name (e.g., Pasta, Biryani, Pancake)")

# --- Generate Recipe ---
if st.button("Generate Recipe"):
    if recipe_name.strip() == "":
        st.warning("Please enter a recipe name.")
    else:
        with st.spinner("Generating recipe..."):
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "X-Title": "AI Recipe Generator"
            }
            payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [{
                    "role": "user",
                    "content": f"Give me a detailed recipe for {recipe_name} including ingredients and instructions."
                }]
            }
            response = requests.post(API_URL, headers=headers, json=payload)

            if response.status_code == 200:
                result = response.json()
                generated_recipe = result["choices"][0]["message"]["content"]
                st.session_state.generated_recipe = generated_recipe
                st.session_state.current_recipe_name = recipe_name
            else:
                st.error("❌ Failed to fetch recipe.")
                st.code(response.text)

# --- Display Generated Recipe ---
if st.session_state.generated_recipe:
    st.markdown(f"<div class='recipe-box'>{st.session_state.generated_recipe}</div>", unsafe_allow_html=True)
