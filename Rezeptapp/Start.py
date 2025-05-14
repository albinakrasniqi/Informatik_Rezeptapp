# ====== Start Init Block ======
# This needs to copied on top of the entry point of the app (Start.py)
import streamlit as st
st.set_page_config(page_title="Emoji-RezeptApp", layout="centered")

import pandas as pd
from utils.data_manager import DataManager
from utils.login_manager import LoginManager

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Rezeptapp2")  # switch drive 

login_manager = LoginManager(data_manager)
login_manager.login_register()


# load the data from the persistent storage into the session state
data_manager.load_user_data(
    session_state_key='data', 
    file_name='recipes.csv', 
    initial_value = pd.DataFrame(),
    encoding='utf-8' 
    )

import streamlit as st

st.markdown("""
<h1 style='text-align: center;'>👋 Willkommen in der Emoji-RezeptApp</h1>
<p style='text-align: center; font-size:20px;'>🍅🥦🐟 Einfach Zutaten per Emoji auswählen <br>
und im Handumdrehen leckere Rezepte entdecken! 🧑‍🍳🍽️</p>
""", unsafe_allow_html=True)

# Rezepte aus dem Session State anzeigen (optional, zur Kontrolle)
data = st.session_state['data']

if data.empty:
    st.markdown("<p style='text-align: center; font-size:20px;'>Keine Rezepte gefunden. Bitte fügen Sie Rezepte hinzu.</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align: center; font-size:20px;'>Hier sind Ihre Rezepte:</p>", unsafe_allow_html=True)
    anzahl = st.slider("Wie viele Rezepte anzeigen?", 10, 500, 5)
    st.dataframe(data.head(anzahl))  # Jetzt ist anzahl sicher definiert