# ====== Start Login Block ======
from utils.login_manager import LoginManager
LoginManager().go_to_login('Start.py')  
# ====== End Login Block ======

import streamlit as st

def kontopage():
    # Titel ganz oben
    st.title("📖 Mein Konto")

    # Diätpräferenzen
    st.markdown("### 🥗 Diätpräferenzen festlegen")
    diät = st.radio(
        "Meine Diät:",
        ["Keine Einschränkung", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"],
        key="diät"
    )

    # Eigene Rezepte anzeigen
    st.markdown("### 📚 Meine Rezepte")
    for i in range(2):
        with st.container():
            st.image("https://source.unsplash.com/600x400/?food", width=300)
            st.write(f"Eigenes Rezept: 🍜🍹🥗")
            st.button("🗑️ Löschen", key=f"my_recipe_{i}")

kontopage()
