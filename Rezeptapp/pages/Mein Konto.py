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

   #erstellte Rezepte
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
                    rezepte = rezepte[rezepte["ID"] != row["ID"]]
                    st.session_state.data = rezepte
                    username = st.session_state.get("username", "default_user")
                    rezepte.to_csv(f"rezepte_{username}.csv", index=False)
                    st.rerun()

kontopage()


