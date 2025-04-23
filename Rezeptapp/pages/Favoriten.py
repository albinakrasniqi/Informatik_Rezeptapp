import streamlit as st

#Textgrösse anpassung

def text(fav):
    st.markdown(f"<p style='font-size:{st.session_state.textgröße}px'>{text}</p>", unsafe_allow_html=True)

def fav():
    st.title("❤️ Meine Favoriten")

    # 🔃 Sortieroptionen
    sort_option = st.selectbox("Sortieren nach", ["Diät", "Mahlzeit", "Zuletzt hinzugefügt", "Alt -> Neu"])

    # 📋 Beispiel-Favoritenliste
    for i in range(2):  # Platzhalter
        with st.container():
            st.image("https://source.unsplash.com/600x400/?dish", width=300)
            st.write("**Favoritenrezept**")
            st.write("Tags: 🥦 Vegan | Mittagessen")
            st.button("🗑️ Entfernen", key=f"remove_{i}")

fav()
