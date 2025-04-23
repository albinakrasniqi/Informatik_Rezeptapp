import streamlit as st

def Kontopage():
    st.title("👤 Mein Konto")


st.markdown("### 🧘 Diätpräferenzen festlegen")
diät = st.radio(
    "Meine Diät",
    ["Keine Einschränkung", "Vegetarisch", "Vegan", "Kein Schweinefleisch"],
    key="diät"
)

st.markdown("### 🔠 Textgröße")
textgröße = st.slider("Textgröße", 12, 24, 16, key="textgröße")

# Beispiel zur Umsetzung der Textgröße:
st.markdown(f"<p style='font-size:{st.session_state.textgröße}px'>Ausgewählte Diät: {st.session_state.diät}</p>", unsafe_allow_html=True)


st.markdown("### 🍳 Meine Rezepte")
for i in range(2):  # Platzhalter
    with st.container():
        st.image("https://source.unsplash.com/600x400/?recipe", width=300)
        st.write("Eigenes Rezept: 🍞🥚🧀")
        st.button("🗑️ Löschen", key=f"my_recipe_{i}")

Kontopage()