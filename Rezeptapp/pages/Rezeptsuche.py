import streamlit as st
import pandas as pd
import uuid  # Für die Generierung von IDs
from utils.data_manager import DataManager  # Falls benötigt, sicherstellen, dass utils verfügbar ist

# Überprüfen, ob Rezeptdaten vorhanden sind
if 'data' not in st.session_state:
    st.warning("📛 Keine Rezeptdaten gefunden. Bitte öffne zuerst die Startseite.")
    st.stop()

# Nur die relevanten Spalten behalten
gewünschte_spalten = [
    "Name", "CookTime", "PrepTime", "TotalTime", "Description", "Images",
    "RecipeCategory", "Keywords", "RecipeIngredientQuantities",
    "RecipeIngredientParts", "RecipeServings", "RecipeInstructions"
]

# Daten aus Session State laden
rezepte = st.session_state['data']
# 🧪 Vorschau auf die Zutatenliste im Datensatz
st.subheader("🧪 Vorschau auf alle Rezeptzutaten")
st.write(rezepte["RecipeIngredientParts"].head(20))  # zeigt die ersten 20 Einträge

# DEBUG: Zeige Struktur
st.write("📊 Shape:", rezepte.shape)
st.write("📋 Spalten:", rezepte.columns.tolist())

# Falls leer, sofort stoppen
if rezepte.empty:
    st.error("❌ Keine Daten im Rezept-Datensatz! Bitte prüfe die Datei in SwitchDrive.")
    st.stop()

# Zutaten-Emoji-Gruppen definieren
zutat_emojis_gruppen = {
    "Kohlenhydrate & Getreide": {
        "🍞": "Brot", "🥖": "Baguette", "🥨": "Brezel", "🍚": "Reis", "🍜": "Nudeln",
        "🫓": "Fladenbrot", "🌽": "Mais", "🍝": "Pasta", "🌰": "Quinoa", "🍢": "Couscous",
        "🥣": "Hirse", "🍥": "Polenta", "🧇": "Haferflocken", "🥯": "Bagel", "🥞": "Pfannkuchen",
        "🌾": "Mehl"
    },
    "Gemüse": {
        "🥦": "Brokkoli", "🥕": "Karotte", "🌶": "Paprika", "🍆": "Aubergine", "🧄": "Knoblauch",
        "🧅": "Zwiebel", "🍄": "Pilze", "🥬": "Blattgemüse", "🥒": "Gurke", "🍅": "Tomate",
        "🫑": "Peperoni", "🥗": "Salat", "🥔": "Kartoffel", "🍠": "Süßkartoffel", "🥬": "Spinat",
        "🎃": "Kürbis", "🥒": "Zucchini", "🥬": "Kohl", "🫛": "Sellerie"
    },
    "Obst": {
        "🍎": "Apfel", "🍐": "Birne", "🍊": "Orange", "🍋": "Zitrone", "🍌": "Banane",
        "🍉": "Wassermelone", "🍇": "Trauben", "🍓": "Erdbeere", "🫐": "Blaubeeren",
        "🥭": "Mango", "🍍": "Ananas", "🥝": "Kiwi", "🍒": "Kirsche", "🍑": "Pfirsich"
    },
    "Eiweissquellen": {
        "🍗": "Poulet", "🥩": "Rindfleisch", "🍖": "Schweinefleisch", "🐟": "Fisch",
        "🦐": "Garnelen", "🧀": "Käse", "🥚": "Ei", "🍳": "Eiweiss", "🥓": "Speck",
        "🧆": "Falafel", "🥫": "Thunfisch", "🍶": "Quark", "🥛": "Joghurt", "🌭": "Wurst",
        "🍢": "Fleischbällchen"
    },
    "Hülsenfrüchte & Nüsse": {
        "🌰": "Haselnüsse", "🥜": "Erdnüsse", "🫘": "Bohnen", "🟤": "Linsen",
        "🟡": "Gelbe Linsen", "🟣": "Schwarze Bohnen", "🟢": "Kichererbsen",
        "🔴": "Rote Linsen", "⚪": "Weiße Bohnen", "💚": "Grüne Erbsen",
        "🌰": "Mandeln", "🌰": "Walnüsse", "🥥": "Kokosnuss"
    },
    "Milchprodukte & Alternativen": {
        "🥛": "Milch", "🧈": "Butter", "🧀": "Käse", "🥥": "Kokosmilch",
        "🌱": "Sojamilch", "🧀": "Parmesan", "🥛": "Sahne", "🧀": "Frischkäse",
        "🥛": "Kondensmilch", "🥛": "Buttermilch"
    },
    "Extras": {
        "🧂": "Salz", "🫒": "Olivenöl", "🍯": "Honig", "🧃": "Essig", "🥫": "Tomatenmark",
        "🍶": "Sojasauce", "🌶": "Chilipulver", "🟤": "Zucker", "🍁": "Ahornsirup",
        "🧁": "Vanilleextrakt", "🍫": "Schokolade", "🍩": "Backpulver", "🍞": "Hefe",
        "🥄": "Senf", "🍯": "Melasse", "🥫": "Worcestersauce", "🍜": "Miso-Paste",
        "🥄": "Tahini", "🧂": "Kreuzkümmel", "🌿": "Thymian", "🌿": "Oregano",
        "🌿": "Rosmarin", "🌿": "Basilikum", "🧂": "Muskatnuss", "🧂": "Zimt"
    }
}

# 🧩 Emoji-Filter
st.markdown("### 🍎 Zutaten auswählen")
st.write("### Was hast du zu Hause?")

# Session State für Auswahl merken
if "auswahl" not in st.session_state:
    st.session_state.auswahl = []

# Zutaten-Auswahl anzeigen
spalten = 5
for gruppe, zutaten in zutat_emojis_gruppen.items():
    st.markdown(f"#### {gruppe}")
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

# 🧘 Diät auswählen
diet = st.selectbox(
    "🧘 Diät wählen",
    ["Alle", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"],
    index=["Alle", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"].index(
        st.session_state.get("diät", "Alle")
    )
)
st.markdown(f"### 🧘 Ausgewählte Diät: {diet}")

# 🍲 Mahlzeittyp auswählen
meal_type = st.selectbox("🍽️ Mahlzeit", ["Alle", "Frühstück", "Mittagessen", "Abendessen", "Snack"])
st.markdown("---")


# Übersetzung Deutsch → Englisch
deutsch_to_englisch = {
    "Brokkoli": "broccoli",
    "Reis": "rice",
    "Karotte": "carrot",
    "Paprika": "bell pepper",
    "Zwiebel": "onion",
    "Knoblauch": "garlic",
    "Tomate": "tomato",
    "Spinat": "spinach",
    "Kartoffel": "potato",
    "Kichererbsen": "chickpeas",
    "Linsen": "lentils",
    "Mais": "corn",
    "Aubergine": "eggplant",
    "Zucchini": "zucchini",
    "Erbsen": "peas",
    "Kohl": "cabbage",
    "Kürbis": "pumpkin"
    # ggf. erweitern
}

st.markdown("### 🔍 Suche starten")
search_button = st.button("🔎 Suchen")

if search_button:
    suchergebnisse = rezepte.copy()

    # Nach Diät filtern
    if diet != "Alle":
        suchergebnisse = suchergebnisse[suchergebnisse['RecipeCategory'].str.contains(diet, case=False, na=False)]

    # Nach Mahlzeittyp filtern
    if meal_type != "Alle":
        suchergebnisse = suchergebnisse[suchergebnisse['MealType'].str.contains(meal_type, case=False, na=False)]

   # Nach Zutaten filtern (mindestens eine muss vorkommen), mit Übersetzung ins Englische
    selected_ingredient_names = [
    deutsch_to_englisch.get(name, name)
    for gruppe in zutat_emojis_gruppen.values()
    for emoji, name in gruppe.items()
    if emoji in selected_ingredients
]

    if selected_ingredient_names:
        suchergebnisse = suchergebnisse[
            suchergebnisse['RecipeIngredientParts'].astype(str).apply(
                lambda x: all(z in x for z in selected_ingredient_names)
            )
        ]


    # Ergebnis anzeigen
    if suchergebnisse.empty:
        st.warning("❌ Kein passendes Rezept gefunden.")
    else:
        st.success(f"✅ {len(suchergebnisse)} Rezept(e) gefunden.")
        st.dataframe(suchergebnisse[["Name", "RecipeCategory", "MealType", "CookTime", "RecipeInstructions"]].head(20))


# Neues Rezept erstellen
if st.button("Neues Rezept erstellen"):
    with st.form("add_recipe_form"):
        rezept_name = st.text_input("📖 Rezepttitel eingeben")
        bild_url = st.text_input("📸 Bild-URL eingeben")
        diät = st.selectbox("🧘 Diät", ["Vegetarisch", "Vegan", "Kein Schweinefleisch"])
        mahlzeit = st.selectbox("🍽 Mahlzeit", ["Frühstück", "Mittagessen", "Abendessen", "Snack"])
        zutaten_emojis = st.multiselect("Zutaten auswählen", list(set([emoji for gruppe in zutat_emojis_gruppen.values() for emoji in gruppe.keys()])))
        zutaten_mit_mengen = st.text_area("Zutaten mit Mengenangaben")
        anleitung = st.text_area("📝 Schritt-für-Schritt Anleitung")
        abgesendet = st.form_submit_button("✅ Rezept speichern")
        
        if abgesendet:
            if not rezept_name:
                st.error("❌ Bitte einen Rezepttitel eingeben.")
            elif not anleitung:
                st.error("❌ Bitte eine Anleitung eingeben.")
            else:
                new_recipe = {
    "RecipeId": str(uuid.uuid4()),
    "Name": rezept_name,
    "Images": bild_url,
    "RecipeIngredientParts": zutaten_emojis,
    "RecipeIngredientQuantities": zutaten_mit_mengen,
    "RecipeInstructions": anleitung,
    "RecipeCategory": diät,
    "MealType": mahlzeit,
    "AuthorId": "user",               # statt 'ErstelltVon'
    "AuthorName": "",                 # falls du keinen Namen angibst
    "TotalTime": "",
    "PrepTime": "",
    "CookTime": "",
    "Description": "",
    "RecipeServings": ""
}

                if 'data' not in st.session_state or st.session_state['data'].empty:
                    st.session_state['data'] = pd.DataFrame([new_recipe])
                else:
                    st.session_state['data'] = pd.concat(
                        [st.session_state['data'], pd.DataFrame([new_recipe])],
                        ignore_index=True
                    )
                st.success("✅ Rezept erfolgreich gespeichert!")

