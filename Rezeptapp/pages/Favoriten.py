import streamlit as st
import pandas as pd
from utils.data_manager import DataManager  # DataManager importieren

# Initialisierung
username = st.session_state.get("username", "gast")
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Rezeptapp2")

# Favoriten aus Datei laden
if "favoriten" not in st.session_state:
    try:
        fav_df = data_manager.load_dataframe(f"favoriten_{username}.csv")
        st.session_state.favoriten = fav_df["ID"].tolist()
    except Exception:
        st.session_state.favoriten = []

def fav():
    st.title("❤️ Meine Favoriten")

    # Rezeptdaten prüfen
    if "data" not in st.session_state or st.session_state["data"].empty:
        st.warning("📛 Keine Rezeptdaten geladen. Bitte öffne zuerst die Startseite.")
        return

    if not st.session_state.favoriten:
        st.info("🧡 Du hast noch keine Favoriten gespeichert.")
        return

    rezepte = st.session_state["data"].copy()

    # Einheitliche ID-Spalte
    if "ID" not in rezepte.columns and "RecipeId" in rezepte.columns:
        rezepte["ID"] = rezepte["RecipeId"]

    # Fehlende Spalten auffüllen
    for col in ["ID", "Name", "Images", "RecipeCategory", "MealType"]:
        if col not in rezepte.columns:
            rezepte[col] = ""

    # Nur Favoriten filtern
    favoriten_df = rezepte[rezepte["ID"].isin(st.session_state.favoriten)].copy()

    # Sortierung
    sort_option = st.selectbox("Sortieren nach", ["Diät", "Mahlzeit", "Zuletzt hinzugefügt", "Alt -> Neu"])
    if st.button("🔃 Sortierung anwenden"):
        if sort_option == "Diät":
            favoriten_df.sort_values(by="RecipeCategory", inplace=True)
        elif sort_option == "Mahlzeit":
            favoriten_df.sort_values(by="MealType", inplace=True)
        elif sort_option in ["Zuletzt hinzugefügt", "Alt -> Neu"]:
            favoriten_df["sort_index"] = favoriten_df["ID"].apply(
                lambda x: st.session_state.favoriten.index(x) if x in st.session_state.favoriten else -1
            )
            favoriten_df.sort_values(by="sort_index", ascending=(sort_option == "Alt -> Neu"), inplace=True)

    # Anzeige der Favoriten
    for _, row in favoriten_df.iterrows():
        with st.container():
            st.markdown(f"### 🍽️ {row.get('Name', '(Kein Titel)')}")
            if pd.notna(row.get("Images", "")) and row["Images"].startswith("http"):
                st.image(row["Images"], width=300)
            st.write(f"🧘 Diät: {row.get('RecipeCategory', '')}")
            st.write(f"🍽️ Mahlzeit: {row.get('MealType', '')}")
            if st.button("🗑️ Entfernen", key=f"remove_fav_{row['ID']}"):
                st.session_state.favoriten.remove(row["ID"])
                # Speichern
                new_fav_df = pd.DataFrame({"ID": st.session_state.favoriten})
                data_manager.save_dataframe(new_fav_df, f"favoriten_{username}.csv")
                st.rerun()

# Seite starten
fav()



