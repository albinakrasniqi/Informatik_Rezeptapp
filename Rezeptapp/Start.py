import streamlit as st
import pandas as pd
from utils.data_manager import DataManager

st.set_page_config(page_title="Emoji-RezeptApp", layout="centered")

data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Rezeptapp2")

# # Daten laden
# data_manager.load_app_data(
#     session_state_key='data', 
#     file_name='recipes.csv', 
#     initial_value=pd.DataFrame(),
#     encoding='utf-8'
# )

# Datensatz bereinigen
def clean_and_validate_data(df):
    required_columns = [
        "ID", "Name", "Images", "RecipeIngredientParts", "RecipeIngredientQuantities",
        "RecipeInstructions", "RecipeCategory", "MealType", "ErstelltVon",
        "TotalTime", "PrepTime", "CookTime", "Description", "RecipeServings"
    ]
    for col in required_columns:
        if col not in df.columns:
            df[col] = None
    return df

st.session_state['data'] = pd.read_csv("data\recipes_sample.csv", on_bad_lines="skip", encoding='utf-8', quotechar='"')
data = clean_and_validate_data(st.session_state['data'])

# Layout
st.markdown("""
<h1 style='text-align: center;'>👋 Willkommen in der Emoji-RezeptApp</h1>
<p style='text-align: center; font-size:20px;'>🍅🥦🐟 Einfach Zutaten per Emoji auswählen <br>
und im Handumdrehen leckere Rezepte entdecken! 🧑‍🍳🍽</p>
""", unsafe_allow_html=True)

# Datenanzeige
if data.empty:
    st.markdown("❗<p style='text-align: center;'>Keine Rezepte gefunden. Bitte fügen Sie Rezepte hinzu.</p>", unsafe_allow_html=True)
else:
    st.markdown("✅ <p style='text-align: center;'>Hier sind Ihre Rezepte:</p>", unsafe_allow_html=True)
    anzahl = st.slider("Wie viele Rezepte anzeigen?", 1, min(len(data), 500), 5)
    st.dataframe(data.head(anzahl))

if st.session_state['data'].empty:
    st.error("❌ Rezept-Datei wurde gefunden, aber sie enthält keine Daten.")
else:
    st.success(f"✅ {len(st.session_state['data'])} Rezepte geladen.")
