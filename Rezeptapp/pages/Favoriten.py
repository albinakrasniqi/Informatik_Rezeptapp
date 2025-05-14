import streamlit as st

def fav():
    st.title("❤️ Meine Favoriten")

    sort_option = st.selectbox("Sortieren nach", ["Diät", "Mahlzeit", "Zuletzt hinzugefügt", "Alt -> Neu"])
    sortieren = st.button("🔃 Sortierung anwenden")

    if "favoriten" not in st.session_state or not st.session_state.favoriten:
        st.info("Noch keine Favoriten gespeichert.")
        return

    rezepte = st.session_state.get('data', pd.DataFrame())
    favoriten_rezepte = rezepte[rezepte["ID"].isin(st.session_state.favoriten)].copy()

    # Nur sortieren, wenn Button gedrückt wurde
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

    for _, row in favoriten_rezepte.iterrows():
        with st.container():
            if "Images" in row and pd.notna(row["Images"]):
                st.image(row["Images"], width=300)
            st.write(f"**{row.get('Name', 'Ohne Titel')}**")
            st.write(f"Tags: {row.get('RecipeCategory', '')} | {row.get('MealType', '')}")
            if st.button("🗑️ Entfernen", key=f"remove_fav_{row['ID']}"):
                st.session_state.favoriten.remove(row["ID"])
                st.experimental_rerun()

