import streamlit as st

def kontopage():
    st.title("👤 Mein Konto")

    st.markdown("### 🥗 Diätpräferenzen festlegen")
    diät = st.radio(
        "Meine Diät:",
        ["Keine Einschränkung", "Vegetarisch", "Vegan", "Kein Schweinefleisch"],
        key="diät"
    )

    st.markdown("### 🔠 Textgröße")

    # Textgröße nur EINMAL setzen (in Session State)
    if "textgröße" not in st.session_state:
        st.session_state.textgröße = 16  # Standardwert

    textgröße = st.slider(
        "Textgröße wählen", 12, 24, st.session_state.textgröße, key="textgröße_slider"
    )
    st.session_state.textgröße = textgröße

    # Sidebar
    with st.sidebar:
        st.markdown("### 🔠 Textgröße")
        st.slider(
            "Textgröße (nur anzeigen)", 12, 24, st.session_state.textgröße, disabled=True
        )

    # Beispiel Textgröße anwenden
    st.markdown(
        f"<p style='font-size:{st.session_state.textgröße}px'>Ausgewählte Diät: {st.session_state.diät}</p>",
        unsafe_allow_html=True
    )

    st.markdown("### 📖 Meine Rezepte")
    for i in range(2):
        with st.container():
            st.image("https://source.unsplash.com/600x400/?food", width=300)
            st.write(f"Eigenes Rezept: 🍝🍜🥗")
            st.button("🗑️ Löschen", key=f"my_recipe_{i}")

kontopage()
