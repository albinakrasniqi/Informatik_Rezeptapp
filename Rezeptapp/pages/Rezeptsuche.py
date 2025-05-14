import streamlit as st
import pandas as pd
import uuid  # ganz oben in deiner Datei, wenn noch nicht da
from utils.data_manager import DataManager 


if 'data' not in st.session_state:
    st.warning("📛 Keine Rezeptdaten gefunden. Bitte öffne zuerst die Startseite.")
    st.stop()

# Nur die relevanten Spalten behalten
gewünschte_spalten = [
    "Name", "CookTime", "PrepTime", "TotalTime", "Description", "Images",
    "RecipeCategory", "Keywords", "RecipeIngredientQuantities",
    "RecipeIngredientParts", "RecipeServings", "RecipeInstructions"
]

# Initialize rezepte from session state data
rezepte = st.session_state['data']
rezepte = rezepte[[spalte for spalte in gewünschte_spalten if spalte in rezepte.columns]]


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
        "🌽": "Mais",
        "🍝": "Pasta",
        "🌰": "Quinoa",
        "🍢": "Couscous",
        "🥣": "Hirse",
        "🍥": "Polenta",
        "🧇": "Haferflocken",
        "🥯": "Bagel",
        "🥞": "Pfannkuchen",
        "🌾": "Mehl"

    },
    "Gemüse": {
        "🥦": "Brokkoli",
        "🥕": "Karotte",
        "🌶": "Paprika",
        "🍆": "Aubergine",
        "🧄": "Knoblauch",
        "🧅": "Zwiebel",
        "🍄": "Pilze",
        "🥬": "Blattgemüse",
        "🥒": "Gurke",
        "🍅": "Tomate",
        "🫑": "Peperoni",
        "🥗": "Salat",
        "🥔": "Kartoffel",
        "🍠": "Süßkartoffel",
        "🥦": "Blumenkohl",
        "🥒": "Zucchini",
        "🥬": "Spinat",
        "🥬": "Kohl",
        "🫛": "Sellerie",
        "🎃": "Kürbis"
    },
    "Obst": {
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
        "🥝": "Kiwi",
        "🍒": "Kirsche",
        "🍑": "Pfirsich"
    },
    "Eiweissquellen": {
        "🍗": "Poulet",
        "🥩": "Rindfleisch",
        "🍖": "Schweinefleisch",
        "🐟": "Fisch",
        "🦐": "Garnelen",
        "🧀": "Käse",
        "🥚": "Ei",
        "🍳": "Eiweiss",
        "🥓": "Speck",
        "🧆": "Falafel",
        "🥫": "Thunfisch",
        "🍶": "Quark",
        "🥛": "Joghurt",
        "🌭": "Wurst",
        "🍢": "Fleischbällchen"
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
        "💚": "Grüne Erbsen",
        "🌰": "Mandeln",
        "🌰": "Walnüsse",
        "🥥": "Kokosnuss"
    },
    "Milchprodukte & Alternativen": {
        "🥛": "Milch",
        "🧈": "Butter",
        "🧀": "Käse",
        "🥥": "Kokosmilch",
        "🌱": "Sojamilch",
        "🧀": "Parmesan",
        "🥛": "Sahne",
        "🧀": "Frischkäse",
        "🥛": "Kondensmilch",
        "🥛": "Buttermilch"
    },
    "Extras": {
        "🧂": "Salz",
        "🫒": "Olivenöl",
        "🍯": "Honig",
        "🧃": "Essig",
        "🥫": "Tomatenmark",
        "🍶": "Sojasauce",
        "🌶": "Chilipulver",
        "🟤": "Zucker",
        "🍁": "Ahornsirup",
        "🧁": "Vanilleextrakt",
        "🍫": "Schokolade",
        "🍩": "Backpulver",
        "🍞": "Hefe",
        "🥄": "Senf",
        "🍯": "Melasse",
        "🥫": "Worcestersauce",
        "🍜": "Miso-Paste",
        "🥄": "Tahini",
        "🧂": "Kreuzkümmel",
        "🌿": "Thymian",
        "🌿": "Oregano",
        "🌿": "Rosmarin",
        "🌿": "Basilikum",
        "🧂": "Muskatnuss",
        "🧂": "Zimt"
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

# Zutaten-Namen aus den Emojis holen
selected_ingredient_names = [
    name for gruppe in zutat_emojis_gruppen.values()
    for emoji, name in gruppe.items() if emoji in selected_ingredients
]

# 🔍 Rezept suchen
if st.button("🔍 Rezept suchen"):
    def zutaten_match(row, zutaten):
        # prüfe, ob alle ausgewählten Zutaten in den Rezept-Zutaten stehen
        if pd.isna(row):
            return False
        return all(any(z.lower() in ingredient.lower() for ingredient in row) for z in zutaten)

    suchergebnisse = rezepte.copy()

    # 🔍 Nach Text im Namen filtern
    if search_term and "Name" in suchergebnisse.columns:
        suchergebnisse = suchergebnisse[suchergebnisse["Name"].str.contains(search_term, case=False, na=False)]

    # 🧘 Nach Diät filtern
    if diet != "Alle" and "RecipeCategory" in suchergebnisse.columns:
        suchergebnisse = suchergebnisse[suchergebnisse["RecipeCategory"] == diet]

    # 🍽️ Nach Mahlzeittyp filtern
    if meal_type != "Alle" and "MealType" in suchergebnisse.columns:
        suchergebnisse = suchergebnisse[suchergebnisse["MealType"] == meal_type]

    # 🧩 Zutatenfilter anwenden
    if selected_ingredient_names:
        if "RecipeIngredientParts" in suchergebnisse.columns:
            suchergebnisse = suchergebnisse[
                suchergebnisse["RecipeIngredientParts"].apply(lambda row: zutaten_match(row, selected_ingredient_names))
            ]
        else:
            st.warning("⚠️ Rezeptdaten enthalten keine Zutateninformationen.")

    # 🔎 Ergebnisse anzeigen
    if suchergebnisse.empty:
        st.warning("❌ Kein passendes Rezept gefunden.")
    else:
        st.success(f"✅ {len(suchergebnisse)} Rezept(e) gefunden")
        for _, row in suchergebnisse.iterrows():
            with st.container():
                if "Images" in row and pd.notna(row["Images"]):
                    st.image(row["Images"], width=300)
                st.markdown(f"### {row.get('Name', 'Ohne Titel')}")
                st.write(f"🕒 Gesamtzeit: {row.get('TotalTime', 'n/a')}")
                st.write(f"📝 Beschreibung: {row.get('Description', '')}")
                st.write(f"📏 Mengen: {row.get('RecipeIngredientQuantities', '')}")
                st.write(f"👨‍🍳 Anleitung: {row.get('RecipeInstructions', '')}")
