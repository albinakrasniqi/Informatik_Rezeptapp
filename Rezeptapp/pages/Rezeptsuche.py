import streamlit as st

def show():
    st.title("🍽️ Rezeptsuche")

    # 🔍 Suchleiste
    search_term = st.text_input("🔍 Suche nach einem Rezept:")
    if search_term:
        st.markdown(f"### 🔍 Suchergebnis für: {search_term}")

    # 🧩 Emoji-Filter
    st.markdown("### 🍎 Zutaten auswählen")

zutat_emojis_gruppen = {
    "🍞 Getreide & Kohlenhydrate": {
        "🍞": "Brot", "🥖": "Baguette", "🥐": "Croissant", "🥨": "Brezel",
        "🍚": "Reis", "🍙": "Reisbällchen", "🍘": "Reiscracker", "🍜": "Nudelsuppe",
        "🍝": "Spaghetti", "🥯": "Bagel", "🥞": "Pfannkuchen", "🧇": "Waffeln", "🫓": "Fladenbrot",
    },
    "🥦 Gemüse": {
        "🥦": "Brokkoli", "🥕": "Karotte", "🌽": "Mais", "🫑": "Paprika", "🍆": "Aubergine",
        "🥬": "Blattgemüse", "🥒": "Gurke", "🧄": "Knoblauch", "🧅": "Zwiebel", "🍄": "Pilze", "🍅": "Tomate", "🥗": "Gemischter Salat",
    },
    "🍎 Obst": {
        "🍎": "Apfel", "🍏": "Grüner Apfel", "🍐": "Birne", "🍊": "Orange", "🍋": "Zitrone",
        "🍌": "Banane", "🍉": "Wassermelone", "🍇": "Trauben", "🍓": "Erdbeere",
        "🫐": "Blaubeeren", "🥭": "Mango", "🍍": "Ananas", "🥝": "Kiwi",
    },
    "🥩 Eiweißquellen": {
        "🥩": "Steak", "🍗": "Hähnchenkeule", "🍖": "Rippchen", "🥓": "Speck", "🦴": "Knochen",
        "🐟": "Fisch", "🦐": "Garnelen", "🦑": "Tintenfisch", "🦞": "Hummer", "🥚": "Ei", "🍳": "Spiegelei", "🌭": "Wurst",
    },
    "🧀 Milchprodukte & Alternativen": {
        "🧀": "Käse", "🥛": "Milch", "🍶": "Reismilch/Sake", "🧈": "Butter", "🍨": "Eiscreme",
        "🍦": "Soft-Eis", "🥤": "Milchshake",
    },
    "🥜 Hülsenfrüchte & Nüsse": {
        "🥜": "Erdnüsse", "🌰": "Kastanien", "🫘": "Bohnen", "🍠": "Süßkartoffel",
    },
    "🍬 Extras": {
        "🧂": "Salz", "🫒": "Olive/Öl", "🧊": "Eiswürfel", "🍫": "Schokolade", "🍯": "Honig",
        "🍪": "Keks", "🍰": "Kuchen", "🍮": "Pudding"
        },
    }

st.write("### Was hast du zu Hause?")

# Session State für Auswahl merken
if "auswahl" not in st.session_state:
    st.session_state.auswahl = []

# Anzahl Spalten pro Reihe
spalten = 5
for gruppe, zutaten in zutat_emojis_gruppen.items():
    st.markdown(f"#### {gruppe}")  # Gruppenüberschrift
    
    emoji_items = list(zutaten.items())
    for i in range(0, len(emoji_items), spalten):
        cols = st.columns(spalten)
        for j, (emoji, name) in enumerate(emoji_items[i:i + spalten]):
            label = f"{emoji} {name}"
            if cols[j].button(label, key=emoji):
                if emoji in st.session_state.auswahl:
                    st.session_state.auswahl.remove(emoji)
                else:
                    st.session_state.auswahl.append(emoji)

# Auswahl anzeigen
selected_ingredients = st.session_state.auswahl
if selected_ingredients:
    st.markdown("### 🛒 Ausgewählte Zutaten")
    st.write(" ".join([f"{emoji} {name}"
                       for gruppe in zutat_emojis_gruppen.values()
                       for emoji, name in gruppe.items()
                       if emoji in selected_ingredients]))
else:
    st.markdown("### 🛒 Keine Zutaten ausgewählt")

    # 🥗 Diätfilter
diet = st.selectbox("🧘 Diät wählen", ["Alle", "Vegetarisch", "Vegan", "Kein Schweinefleisch"])

    # Display selected diet
st.markdown(f"### 🧘 Ausgewählte Diät: {diet}")

    # 🍲 Mahlzeittyp
meal_type = st.selectbox("🍽️ Mahlzeit", ["Alle", "Frühstück", "Mittagessen", "Abendessen", "Snack"])

st.markdown("---")

    # 📋 Dummy-Rezeptanzeige
st.subheader("🔎 Gefundene Rezepte")
st.markdown(f"### 🍽️ Ausgewählter Mahlzeittyp: {meal_type}")
for i in range(2):  # Platzhalter für Demo
     with st.container():
            st.image("https://source.unsplash.com/600x400/?food", width=300)
            st.write("**Rezepttitel**")
            st.write("Treffer: 🥕 🍝")
            if st.button("❤️ Zu Favoriten", key=f"fav_{i}"):
                st.success("Zum Favoriten hinzugefügt")

    # ➕ Rezept hinzufügen
st.markdown("### ➕ Rezept hinzufügen")
if st.button("Neues Rezept erstellen"):
        with st.form("add_recipe_form"):
            st.text_input("📸 Bild-URL eingeben")
            st.selectbox("🧘 Diät", ["Vegetarisch", "Vegan", "Kein Schweinefleisch"])
            st.selectbox("🍽️ Mahlzeit", ["Frühstück", "Mittagessen", "Abendessen", "Snack"])
            st.multiselect("Zutaten auswählen", zutat_emojis)
            st.text_area("Zutaten mit Mengenangaben")
            st.text_area("📝 Schritt-für-Schritt Anleitung")
            st.form_submit_button("✅ Rezept speichern")

