import streamlit as st
import json

st.title("🔍 Rezepte suchen")

# JSON-Datei laden
with open("data/rezepte.json", "r", encoding="utf-8") as f:
    rezepte = json.load(f)

# Emoji-Auswahl
auswahl = st.multiselect("Wähle Zutaten (Emojis):", ["🥦", "🥕", "🐟", "🍗", "🍚", "🍅", "🧀", "🥚", "🥩", "🍞"])

# Gefilterte Rezepte anzeigen
if auswahl:
    gefundene_rezepte = [r for r in rezepte if set(auswahl).issubset(set(r["zutaten"]))]
    if gefundene_rezepte:
        st.success(f"{len(gefundene_rezepte)} passende Rezepte gefunden:")
        for rezept in gefundene_rezepte:
            st.subheader(rezept["titel"])
            st.write("🍽️ Zutaten:", " ".join(rezept["zutaten"]))
            st.write(rezept["beschreibung"])
            if rezept["bild_url"]:
                st.image(rezept["bild_url"])
            st.markdown("---")
    else:
        st.warning("Keine passenden Rezepte gefunden.")
else:
    st.info("⬅️ Bitte wähle Emojis aus, um passende Rezepte zu sehen.")
