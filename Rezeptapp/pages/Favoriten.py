import streamlit as st
import pandas as pd  # Fehlender Import

def fav():
    st.title("❤️ Meine Favoriten")

    # Rezeptdaten prüfen und laden
    if "data" not in st.session_state or st.session_state["data"].empty:
        st.warning("📛 Keine Rezeptdaten geladen. Bitte öffne zuerst die Startseite.")
        return

    # Favoriten initialisieren, wenn noch nicht vorhanden
    if "favoriten" not in st.session_state:
        st.session_state.favoriten = []

    # Wenn keine Favoriten vorhanden sind
    if not st.session_state.favoriten:
        st.info("🩷 Du hast noch keine Favoriten gespeichert.")
        return

    # Daten kopieren
    rezepte = st.session_state['data'].copy()

    # Einheitliche ID-Spalte sicherstellen
    if "ID" not in rezepte.columns and "RecipeId" in rezepte.columns:
        rezepte["ID"] = rezepte["RecipeId"]

    # Fehlende Spalten auffüllen
    required_cols = ["ID", "Name", "Images", "RecipeCategory", "MealType"]
    for col in required_cols:
        if col not in rezepte.columns:
            rezepte[col] = ""

    # Nur Favoriten herausfiltern
    favoriten_rezepte = rezepte[rezepte["ID"].isin(st.session_state.favoriten)].copy()

    # Sortieren
    sort_option = st.selectbox("Sortieren nach", ["Diät", "Mahlzeit", "Zuletzt hinzugefügt", "Alt -> Neu"])
    if st.button("🔃 Sortierung anwenden"):
        if sort_option == "Diät":
            favoriten_rezepte.sort_values(by="RecipeCategory", inplace=True)
        elif sort_option == "Mahlzeit":
            favoriten_rezepte.sort_values(by="MealType", inplace=True)
        elif sort_option in ["Zuletzt hinzugefügt", "Alt -> Neu"]:
            favoriten_rezepte["sort_index"] = favoriten_rezepte["ID"].apply(
                lambda x: st.session_state.favoriten.index(x) if x in st.session_state.favoriten else -1
            )
            favoriten_rezepte.sort_values(
                by="sort_index",
                ascending=(sort_option == "Alt -> Neu"),
                inplace=True
            )

    # Favoriten anzeigen
    for _, row in favoriten_rezepte.iterrows():
        with st.container():
            st.markdown(f"### 🍽️ {row.get('Name', 'Ohne Titel')}")
            if "Images" in row and pd.notna(row["Images"]) and row["Images"].startswith("http"):
                st.image(row["Images"], width=300)
            st.write(f"🧘 Diät: {row.get('RecipeCategory', '')}")
            st.write(f"🍽️ Mahlzeit: {row.get('MealType', '')}")
            if st.button("🗑️ Entfernen", key=f"remove_fav_{row['ID']}"):
                st.session_state.favoriten.remove(row["ID"])
                st.rerun()

# ⬅️ Hier aufrufen
fav()


