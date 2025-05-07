import streamlit as st
if 'data' not in st.session_state:
    st.warning("📛 Keine Rezeptdaten gefunden. Bitte öffne zuerst die Startseite.")
    st.stop()


#Textgrösse anpassung

def text(text):
    st.markdown(f"<p style='font-size:{st.session_state.textgröße}px'>{text}</p>", unsafe_allow_html=True)

# Extract all emojis from zutat_emojis_gruppen
def show():
    st.title("🍽️ Rezeptsuche")

zutat_emojis_gruppen = {
    "Kohlenhydrate & Getreide": {
        "🍞": "Brot",
        "🥖": "Baguette",
        "🥨": "Brezel",
        "🍚": "Reis",
        "🍜": "Nudeln",
        "🫓": "Fladenbrot",
        "🌾": "Hafer",
        "🌽": "Mais"
    },
    "Gemüse": {
        "🥦": "Brokkoli",
        "🥕": "Karotte",
        "🌶️": "Paprika",
        "🍆": "Aubergine",
        "🧄": "Knoblauch",
        "🧅": "Zwiebel",
        "🍄": "Pilze",
        "🥬": "Blattgemüse",
        "🥒": "Gurke",
        "🍅": "Tomate",
        "🫑": "Peperoni",
        "🥗": "Salat"
    },
    "Obst": {
        "🍏": "Grüner Apfel",
        "🍎": "Apfel",
        "🍐": "Birne",
        "🍊": "Orange",
        "🍋": "Zitrone",
        "🍌": "Banane",
        "🍉": "Wassermelone",
        "🍇": "Trauben",
        "🍓": "Erdbeere",
        "🫐": "Blaubeeren",
        "🥭": "Mango",
        "🍍": "Ananas",
        "🥝": "Kiwi"
    },
    "Eiweissquellen": {
        "🍗": "Poulet",
        "🥩": "Rindfleisch",
        "🍖": "Schweinefleisch",
        "🐟": "Fisch",
        "🦐": "Garnelen",
        "🧀": "Käse",
        "🥚": "Ei",
        "🍳": "Eiklar"
    },
    "Hülsenfrüchte & Nüsse": {
        "🌰": "Haselnüsse",
        "🥜": "Erdnüsse",
        "🫘": "Bohnen",
        "🍠": "Süßkartoffel",
        "🟤": "Linsen",
        "🟡": "Gelbe Linsen",
        "🟣": "Schwarze Bohnen",
        "🟢": "Kichererbsen",
        "🔴": "Rote Linsen",
        "⚪": "Weiße Bohnen",
        "💚": "Grüne Erbsen"
    },
    "Milchprodukte & Alternativen": {
        "🥛": "Milch",
        "🧈": "Butter",
        "🧀": "Käse",
        "🍦": "Eis",
        "🥥": "Kokosmilch",
        "🌱": "Sojamilch"
    },
    "Extras": {
        "🧂": "Salz",
        "🫒": "Olivenöl",
        "🍯": "Honig"
    }
}

zutat_emojis = [emoji for gruppe in zutat_emojis_gruppen.values() for emoji in gruppe.keys()]

    # 🔍 Suchleiste
search_term = st.text_input("🔍 Suche nach einem Rezept:")
if search_term:
        st.markdown(f"### 🔍 Suchergebnis für: {search_term}")

# 🧩 Emoji-Filter
st.markdown("### 🍎 Zutaten auswählen")

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
            if cols[j].button(label, key=f"{gruppe}_{emoji}"):
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
diet = st.selectbox("🧘 Diät wählen", ["Alle", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"])

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


if st.button("Rezept suchen"):
    st.subheader("🔎 Gefundene Rezepte")
    
    rezepte = st.session_state['data']  # das geladene DataFrame
    zutaten = st.session_state.auswahl  # ausgewählte Emojis
    st.write(rezepte.columns.tolist())

if 'RecipeIngredientParts' in rezepte.columns:
    gefundene = rezepte[rezepte['RecipeIngredientParts'].apply(
        lambda z: all(zutat in str(z) for zutat in zutaten)
    )]
    if gefundene.empty:
        st.warning("❌ Kein passendes Rezept gefunden.")
    else:
        for i, row in gefundene.iterrows():
            with st.container():
                st.image(row['Images'], width=300)
                st.markdown(f"**{row['Name']}**")
                st.write(f"🍽️ Zutaten: {row['RecipeIngredientParts']}")
                st.write(f"📝 Zubereitung: {row['RecipeInstructions']}")
                if st.button("❤️ Zu Favoriten", key=f"fav_{row['ID']}"):
                    st.success("Zum Favoriten hinzugefügt")
else:
    st.error("❌ Die Spalte 'RecipeIngredientParts' wurde nicht gefunden.")
    st.write("📋 Verfügbare Spalten:", rezepte.columns.tolist())
    st.stop()
rezepte = st.session_state['data']  # das geladene DataFrame
zutaten = st.session_state.auswahl  # ausgewählte Emojis
