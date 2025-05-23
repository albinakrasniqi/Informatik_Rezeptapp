import streamlit as st
import pandas as pd
import io
import requests
from requests.auth import HTTPBasicAuth




def kontopage():
    st.title("📖 Mein Konto")

#Diätpräferenzen
    st.markdown("### 🥗 Diätpräferenzen festlegen")
    diät = st.radio(
        "Meine Diät:",
        ["Alle", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"],
        key="diätform"
    )
    if st.button("Diätform speichern", key="save_diet"):
        st.session_state['gespeicherte_diätform'] = diät
        st.success(f"Diätform '{diät}' wurde gespeichert!")
    # Beim Seitenaufruf: Wenn gespeichert, setze diätform auf gespeicherten Wert
    if 'gespeicherte_diätform' in st.session_state and st.session_state['diätform'] != st.session_state['gespeicherte_diätform']:
        st.session_state['diätform'] = st.session_state['gespeicherte_diätform']

# Eigene Rezepte
    username = st.session_state.get("username", "user")
    base_url = st.secrets["webdav"]["base_url"]
    webdav_user = st.secrets["webdav"]["username"]
    webdav_password = st.secrets["webdav"]["password"]
    url = f"{base_url}/files/{webdav_user}/rezepte_{username}.csv"
    auth = HTTPBasicAuth(webdav_user, webdav_password)
    try:
        response = requests.get(url, auth=auth)
        if response.status_code == 200:
            rezepte = pd.read_csv(io.StringIO(response.text))
        else:
            rezepte = pd.DataFrame()
    except Exception as e:
        st.error(f"Fehler beim Laden der Rezepte: {e}")
        rezepte = pd.DataFrame()
    st.session_state["data"] = rezepte

    # Jetzt kannst du die Rezepte anzeigen:
    if not rezepte.empty:
        st.markdown("### Deine eigenen Rezepte")
        st.dataframe(rezepte)
    else:
        st.info("Noch keine eigenen Rezepte gespeichert.")
        
kontopage()


