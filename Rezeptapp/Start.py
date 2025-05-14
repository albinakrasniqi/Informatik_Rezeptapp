import streamlit as st
import pandas as pd

from utils.data_manager import DataManager


# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Rezeptapp2")  # switch drive 

# load the data from the persistent storage into the session state
data_manager.load_app_data(
    session_state_key='data', 
    file_name='recipes.csv', 
    initial_value = pd.DataFrame(),
    encoding='utf-8' 
    )

import streamlit as st


st.set_page_config(page_title="Emoji-RezeptApp", layout="centered")

st.markdown("""
<h1 style='text-align: center;'>👋 Willkommen in der Emoji-RezeptApp</h1>
<p style='text-align: center; font-size:20px;'>🍅🥦🐟 Einfach Zutaten per Emoji auswählen <br>
und im Handumdrehen leckere Rezepte entdecken! 🧑‍🍳🍽️</p>
""", unsafe_allow_html=True)

data = st.session_state['data']
if data.empty:
    st.markdown("<p style='text-align: center; font-size:20px;'>Keine Rezepte gefunden. Bitte fügen Sie Rezepte hinzu.</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align: center; font-size:20px;'>Hier sind Ihre Rezepte:</p>", unsafe_allow_html=True)
    anzahl = st.slider("Wie viele Rezepte anzeigen?", 10, 500, 10)
    st.dataframe(data.head(anzahl))  # Jetzt ist anzahl sicher definiert

# Gewünschte Spalten definieren
gewünschte_spalten = [
    "Name",
    "CookTime",
    "PrepTime",
    "TotalTime",
    "Description", 
    "RecipeCategory",
    "Keywords",
    "RecipeIngredientQuantities",
    "RecipeIngredientParts",
    "RecipeServings",
    "RecipeInstructions"
]

# Nur vorhandene Spalten auswählen, um Fehler zu vermeiden
vorhandene_spalten = [spalte for spalte in gewünschte_spalten if spalte in data.columns]

# Gewünschte Anzahl anzeigen
anzahl = st.slider("Wie viele Rezepte anzeigen?", 1, min(len(data), 500), 5)
st.dataframe(data[vorhandene_spalten].head(anzahl))



