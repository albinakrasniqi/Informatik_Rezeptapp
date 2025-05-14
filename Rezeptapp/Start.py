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
data_manager.load_app_data(
    session_state_key='data', 
    file_name='recipes.csv', 
    initial_value = pd.DataFrame(),
    encoding='utf-8' 
    )
st.write("✅ Daten geladen:")
st.write(st.session_state['data'].shape)
st.write(st.session_state['data'].head(3))

import streamlit as st

st.markdown("""
<h1 style='text-align: center;'>👋 Willkommen in der Emoji-RezeptApp</h1>
<p style='text-align: center; font-size:20px;'>🍅🥦🐟 Einfach Zutaten per Emoji auswählen <br>
und im Handumdrehen leckere Rezepte entdecken! 🧑‍🍳🍽️</p>
""", unsafe_allow_html=True)

