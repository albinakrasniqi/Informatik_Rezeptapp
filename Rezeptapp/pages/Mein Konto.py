import streamlit as st

def show():
    st.title("👤 Mein Konto")

    st.markdown("### 🧘 Diätpräferenzen festlegen")
    st.radio("Meine Diät", ["Keine Einschränkung", "Vegetarisch", "Vegan", "Kein Schweinefleisch"])

    st.markdown("### 🔠 Textgröße")
    st.slider("Textgröße", 12, 24, 16)

    st.markdown("### 🍳 Meine Rezepte")
    for i in range(2):  # Platzhalter
        with st.container():
            st.image("https://source.unsplash.com/600x400/?recipe", width=300)
            st.write("Eigenes Rezept: 🍞🥚🧀")
            st.button("🗑️ Löschen", key=f"my_recipe_{i}")
