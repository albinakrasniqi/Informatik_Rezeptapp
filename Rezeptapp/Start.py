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

st.title("👋 Hallo zur Emoji-RezeptApp")
st.write("Hier kannst du mit Emojis deine Zutaten auswählen und passende Rezepte finden.")