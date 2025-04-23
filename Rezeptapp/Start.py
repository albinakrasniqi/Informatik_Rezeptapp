import streamlit as st
import pandas as pd

from utils.data_manager import DataManager

# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="BMLD_App_DB")  # switch drive 

# load the data from the persistent storage into the session state
data_manager.load_app_data(
    session_state_key='data_df', 
    file_name='data.csv', 
    initial_value = pd.DataFrame(), 
    parse_dates = ['timestamp']
    )


import streamlit as st

st.set_page_config(page_title="Emoji-RezeptApp", layout="centered")

st.markdown("""
<h1 style='text-align: center;'>👋 Willkommen in der Emoji-RezeptApp</h1>
<p style='text-align: center; font-size:20px;'>🍅🥦🐟 Einfach Zutaten per Emoji auswählen <br>
und im Handumdrehen leckere Rezepte entdecken! 🧑‍🍳🍽️</p>
""", unsafe_allow_html=True)

import streamlit as st
import home
import favorites
import profile

# Seitenmenü in der Sidebar
page = st.sidebar.selectbox("Seite wählen", ["Start", "Favoriten", "Profil"])

if page == "Rezeptsuche":
    home.show()
elif page == "Favoriten":
    favorites.show()
elif page == "Mein Konto":
    profile.show()

