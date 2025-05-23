import streamlit as st
import pandas as pd
from .. import data_manager  # Adjust the import path as needed


def kontopage():
    st.title("📖 Mein Konto")

    # fürs Speichern von erstellten Rezepten
    username = st.session_state.get("username", "default_user")
    rezepte = data_manager.load_data(f"rezepte_{username}.csv")
    st.session_state["data"] = rezepte


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

   
    st.markdown("### 📚 Meine Rezepte")

    rezepte = st.session_state.get("data", pd.DataFrame())
    if "ErstelltVon" not in rezepte.columns:
        st.warning("⚠ Keine gültigen Rezeptdaten gefunden.")
        return



    eigene_rezepte = rezepte[rezepte["ErstelltVon"] == "user"]

    if eigene_rezepte.empty:
        st.info("Noch keine eigenen Rezepte erstellt.")
    else:
        for _, row in eigene_rezepte.iterrows():
            with st.container():
                if "Images" in row and pd.notna(row["Images"]):
                    st.image(row["Images"], width=300)
                st.write(f"**{row.get('Name', 'Ohne Titel')}**")
                st.write(f"Tags: {row.get('RecipeCategory', '')} | {row.get('MealType', '')}")
                if st.button("🗑 Löschen", key=f"my_recipe_{row['ID']}"):
                    st.session_state.data = rezepte[rezepte["ID"] != row["ID"]]
                    st.rerun()
    username = st.session_state.get("username", "default_user")
    st.session_state["data"] = data_manager.load_data(f"rezepte_{username}.csv")


kontopage()


