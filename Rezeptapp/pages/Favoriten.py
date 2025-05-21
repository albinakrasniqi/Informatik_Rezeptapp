import streamlit as st
import pandas as pd  # Fehlender Import

def fav():
    st.title("❤️ Meine Favoriten")

    sort_option = st.selectbox("Sortieren nach", ["Diät", "Mahlzeit", "Zuletzt hinzugefügt", "Alt -> Neu"])
    sortieren = st.button("🔃 Sortierung anwenden")

    # Initialisiere Favoriten, falls nicht vorhanden
    if "favoriten" not in st.session_state:
        st.session_state.favoriten = []

    if not st.session_state.favoriten:
        st.info("Noch keine Favoriten gespeichert.")
        return

    # Lade Rezeptdaten
    rezepte = st.session_state.get('data', pd.DataFrame())
    if rezepte.empty or "ID" not in rezepte.columns:
        st.warning("⚠️ Keine gültigen Rezeptdaten gefunden.")
        return
    rezepte = rezepte if not rezepte.empty else pd.DataFrame()
    required_cols = ["ID", "Name", "Images", "RecipeCategory", "MealType"]
    for col in required_cols:
        if col not in rezepte.columns:
            rezepte[col] = ""
    # Einheitliche ID-Spalte sicherstellen
    if "ID" not in rezepte.columns and "RecipeId" in rezepte.columns:
        rezepte["ID"] = rezepte["RecipeId"]

    # Filtere Favoriten
    favoriten_rezepte = rezepte[rezepte["ID"].isin(st.session_state.favoriten)].copy()

    # Sortieren
    if sortieren:
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
            if "Images" in row and pd.notna(row["Images"]):
                st.image(row["Images"], width=300)
            st.write(f"**{row.get('Name', 'Ohne Titel')}**")
            st.write(f"Tags: {row.get('RecipeCategory', '')} | {row.get('MealType', '')}")
            if st.button("🗑️ Entfernen", key=f"remove_fav_{row['ID']}"):
                st.session_state.favoriten.remove(row["ID"])
                st.rerun()

fav() 

