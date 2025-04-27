import streamlit as st

def kontopage():
    st.title("👤 Mein Konto")

    st.markdown("### 🍴 Diätpräferenzen festlegen")
    diät = st.radio(
        "Meine Diät:",
        ["Keine Einschränkung", "Vegetarisch", "Vegan", "Kein Schweinefleisch"],
        key="diät"
    )

    st.markdown("### 🧡 Meine Rezepte")
    for i in range(2):
        with st.container():
            st.image("https://source.unsplash.com/600x400/?food", width=300)
            st.write("🍴 Eigenes Rezept: 🍅🥬🐟")
            st.button("🗑️ Löschen", key=f"my_recipe_{i}")

kontopage()
