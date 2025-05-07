import streamlit as st
import pandas as pd

from utils.data_manager import DataManager

#Textgrösse anpassung

def text(text):
    st.markdown(f"<p style='font-size:{st.session_state.textgröße}px'>{text}</p>", unsafe_allow_html=True)

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
    # Display the data in a table format
    anzahl = st.slider("Wie viele Rezepte anzeigen?", 10, 500, 100)
st.table(data.head(anzahl))
  # Display the data in a table format




