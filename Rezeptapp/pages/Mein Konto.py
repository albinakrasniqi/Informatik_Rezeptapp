import streamlit as st

def kontopage():
    st.title("📖 Mein Konto")

    st.markdown("### 🥗 Diätpräferenzen festlegen")
    diät = st.radio(
        "Meine Diät:",
        ["Keine Einschränkung", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"],
        key="diät"
    )

    st.markdown("### 📚 Meine Rezepte")

    rezepte = st.session_state.get("data", pd.DataFrame())
    eigene_rezepte = rezepte[rezepte.get("ErstelltVon") == "user"]

    if eigene_rezepte.empty:
        st.info("Noch keine eigenen Rezepte erstellt.")
    else:
        for _, row in eigene_rezepte.iterrows():
            with st.container():
                if "Images" in row and pd.notna(row["Images"]):
                    st.image(row["Images"], width=300)
                st.write(f"**{row.get('Name', 'Ohne Titel')}**")
                st.write(f"Tags: {row.get('RecipeCategory', '')} | {row.get('MealType', '')}")
                if st.button("🗑️ Löschen", key=f"my_recipe_{row['ID']}"):
                    st.session_state.data = rezepte[rezepte["ID"] != row["ID"]]
                    st.experimental_rerun()

