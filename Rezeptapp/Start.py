import streamlit as st
import pandas as pd
from utils.data_manager import DataManager
import os

st.set_page_config(page_title="Emoji-RezeptApp", layout="centered")


# Initialisiere den DataManager (nicht aktiv genutzt bei lokalem Laden)
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Rezeptapp2")

# load the data from the persistent storage into the session state
data_manager.load_app_data(
    session_state_key='data', 
    file_name='recipes.csv', 
    initial_value = pd.DataFrame(),
    encoding='utf-8' 
    )

# Layout
st.markdown("""
<h1 style='text-align: center;'>👋 Willkommen in der Emoji-RezeptApp</h1>
<p style='text-align: center; font-size:20px;'>🍅🥦🐟 Einfach Zutaten per Emoji auswählen <br>
und im Handumdrehen leckere Rezepte entdecken! 🧑‍🍳🍽️</p>
""", unsafe_allow_html=True)

# Datenanzeige
data = st.session_state['data']
if data.empty:
    st.markdown("❗<p style='text-align: center;'>Keine Rezepte gefunden. Bitte fügen Sie Rezepte hinzu.</p>", unsafe_allow_html=True)
else:
    st.markdown("✅ <p style='text-align: center;'>Hier sind Ihre Rezepte:</p>", unsafe_allow_html=True)
    anzahl = st.slider("Wie viele Rezepte anzeigen?", 1, min(len(data), 500), 5)
    st.dataframe(data.head(anzahl))
