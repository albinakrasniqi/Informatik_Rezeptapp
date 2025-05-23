import streamlit as st
import pandas as pd



def kontopage():
    st.title("📖 Mein Konto")

    # fürs Speichern von erstellten Rezepten
    username = st.session_state.get("username", "default_user")
    try:
        rezepte = pd.read_csv(f"rezepte_{username}.csv")
    except Exception:
        rezepte = pd.DataFrame()
    st.session_state["data"] = rezepte

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

   
        

kontopage()


