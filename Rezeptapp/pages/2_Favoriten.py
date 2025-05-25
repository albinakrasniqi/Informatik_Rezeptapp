import streamlit as st
import pandas as pd
import os


# Initialisierung
username = st.session_state.get("username", "gast")

pfad = os.path.join(".", f"favoriten_{username}.csv")

def fav():
    st.title("❤️ Meine Favoriten")

    if "data" not in st.session_state or st.session_state["data"].empty:
        st.warning("📛 Keine Rezeptdaten geladen. Bitte öffne zuerst die Startseite.")
        return

    if not st.session_state.favoriten:
        st.info("🧡 Du hast noch keine Favoriten gespeichert.")
        return

    rezepte = st.session_state["data"].copy()

    if "ID" not in rezepte.columns and "RecipeId" in rezepte.columns:
        rezepte["ID"] = rezepte["RecipeId"]

    for col in ["ID", "Name", "Images", "RecipeCategory", "MealType"]:
        if col not in rezepte.columns:
            rezepte[col] = ""

    favoriten_df = rezepte[rezepte["ID"].isin(st.session_state.favoriten)].copy()

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

    for _, row in favoriten_df.iterrows():
        with st.container():
            st.markdown(f"### 🍽️ {row.get('Name', '(Kein Titel)')}")
            if pd.notna(row.get("Images", "")) and row["Images"].startswith("http"):
                st.image(row["Images"], width=300)
            st.write(f"🧘 Diät: {row.get('RecipeCategory', '')}")
            st.write(f"🍽️ Mahlzeit: {row.get('MealType', '')}")
            if st.button("🗑️ Entfernen", key=f"remove_fav_{row['ID']}"):
                st.session_state.favoriten.remove(row["ID"])
                new_fav_df = pd.DataFrame({"ID": st.session_state.favoriten})
                new_fav_df.to_csv(pfad, index=False)
                st.rerun()

# Seite starten
fav()



