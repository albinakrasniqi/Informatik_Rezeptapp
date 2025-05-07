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

import uuid  # ganz oben in deiner Datei, wenn noch nicht da
import pandas as pd

if st.button("Neues Rezept erstellen"):
    with st.form("add_recipe_form"):
        bild_url = st.text_input("📸 Bild-URL eingeben")
        diät = st.selectbox("🧘 Diät", ["Vegetarisch", "Vegan", "Kein Schweinefleisch"])
        mahlzeit = st.selectbox("🍽️ Mahlzeit", ["Frühstück", "Mittagessen", "Abendessen", "Snack"])
        zutaten_emojis = st.multiselect("Zutaten auswählen", zutat_emojis)
        zutaten_mit_mengen = st.text_area("Zutaten mit Mengenangaben")
        anleitung = st.text_area("📝 Schritt-für-Schritt Anleitung")

        abgesendet = st.form_submit_button("✅ Rezept speichern")
        if abgesendet:
            new_recipe = {
                "ID": str(uuid.uuid4()),
                "Name": "Rezepttitel",  # Hier kannst du noch ein Feld für den Titel hinzufügen
                "Images": bild_url,
                "RecipeIngredientParts": zutaten_emojis,
                "RecipeInstructions": anleitung,
                "RecipeCategory": diät,
                "MealType": mahlzeit
            }

            # Stelle sicher, dass die DataFrame-Struktur da ist
            if 'data' not in st.session_state or st.session_state['data'].empty:
                st.session_state['data'] = pd.DataFrame([new_recipe])
            else:
                st.session_state['data'] = pd.concat(
                    [st.session_state['data'], pd.DataFrame([new_recipe])],
                    ignore_index=True
                )

            st.success("✅ Rezept erfolgreich gespeichert!")

if st.button("Rezept suchen"):
    st.subheader("🔎 Gefundene Rezepte")

    rezepte = st.session_state.get('data', None)
    st.write(rezepte[['Name', 'RecipeIngredientParts']].head(5))
    zutaten = st.session_state.get('auswahl', [])

    if rezepte is None or rezepte.empty:
        st.error("⚠️ Keine Rezepte geladen.")
        st.stop()

    # Spalten zur Kontrolle anzeigen
    st.write("📋 Verfügbare Spalten:", rezepte.columns.tolist())

    if 'RecipeIngredientParts' in rezepte.columns:
        # Filter: nur Rezepte mit allen ausgewählten Zutaten
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
        st.stop()
