import streamlit as st
import pandas as pd
import uuid  # Für die Generierung von IDs
from utils.data_manager import DataManager  # Falls benötigt, sicherstellen, dass utils verfügbar ist
import re
import ast


if "favoriten" not in st.session_state:
    st.session_state.favoriten = []


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
# Hole die gespeicherte Diätform, falls vorhanden, sonst 'Alle'
if 'gespeicherte_diätform' in st.session_state:
    default_diet = st.session_state['gespeicherte_diätform']
else:
    default_diet = 'Alle'
diet = st.selectbox(
    "🧘 Diät wählen",
    ["Alle", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"],
    index=["Alle", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"].index(default_diet),
    key="rezeptsuche_diätform"
)
st.session_state['diätform'] = diet
st.markdown(f"### 🧘 Ausgewählte Diät: {diet}")

# 🍲 Mahlzeittyp auswählen
meal_type = st.selectbox("🍽️ Mahlzeit", ["Alle", "Frühstück", "Mittagessen", "Abendessen", "Snack"])
st.markdown("---")


# Übersetzung Deutsch → Englisch
deutsch_to_englisch = {
    # Kohlenhydrate & Getreide
    "Brot": "bread", "Baguette": "baguette", "Brezel": "pretzel", "Reis": "rice", "Nudeln": "noodles",
    "Fladenbrot": "flatbread", "Mais": "corn", "Pasta": "pasta", "Quinoa": "quinoa", "Couscous": "couscous",
    "Hirse": "millet", "Polenta": "polenta", "Haferflocken": "oatmeal", "Bagel": "bagel", "Pfannkuchen": "pancake",
    "Mehl": "flour",

    # Gemüse
    "Brokkoli": "broccoli", "Karotte": "carrot", "Paprika": "bell pepper", "Aubergine": "eggplant",
    "Knoblauch": "garlic", "Zwiebel": "onion", "Pilze": "mushrooms", "Blattgemüse": "leafy greens",
    "Gurke": "cucumber", "Tomate": "tomato", "Peperoni": "chili pepper", "Salat": "lettuce",
    "Kartoffel": "potato", "Süßkartoffel": "sweet potato", "Spinat": "spinach", "Kürbis": "pumpkin",
    "Zucchini": "zucchini", "Kohl": "cabbage", "Sellerie": "celery",

    # Obst
    "Apfel": "apple", "Birne": "pear", "Orange": "orange", "Zitrone": "lemon", "Banane": "banana",
    "Wassermelone": "watermelon", "Trauben": "grapes", "Erdbeere": "strawberry", "Blaubeeren": "blueberries",
    "Mango": "mango", "Ananas": "pineapple", "Kiwi": "kiwi", "Kirsche": "cherry", "Pfirsich": "peach",

    # Eiweissquellen
    "Poulet": "chicken", "Rindfleisch": "beef", "Schweinefleisch": "pork", "Fisch": "fish",
    "Garnelen": "shrimp", "Käse": "cheese", "Ei": "egg", "Eiweiss": "egg white", "Speck": "bacon",
    "Falafel": "falafel", "Thunfisch": "tuna", "Quark": "quark", "Joghurt": "yogurt",
    "Wurst": "sausage", "Fleischbällchen": "meatballs",

    # Hülsenfrüchte & Nüsse
    "Haselnüsse": "hazelnuts", "Erdnüsse": "peanuts", "Bohnen": "beans", "Linsen": "lentils",
    "Gelbe Linsen": "yellow lentils", "Schwarze Bohnen": "black beans", "Kichererbsen": "chickpeas",
    "Weiße Bohnen": "white beans", "Grüne Erbsen": "green peas", "Erbsen": "peas",
    "Mandeln": "almonds", "Walnüsse": "walnuts", "Kokosnuss": "coconut",

    # Milchprodukte & Alternativen
    "Milch": "milk", "Butter": "butter", "Kokosmilch": "coconut milk", "Sojamilch": "soy milk",
    "Parmesan": "parmesan", "Sahne": "cream", "Frischkäse": "cream cheese", "Kondensmilch": "condensed milk",
    "Buttermilch": "buttermilk",

    # Extras
    "Salz": "salt", "Olivenöl": "olive oil", "Honig": "honey", "Essig": "vinegar", "Tomatenmark": "tomato paste",
    "Sojasauce": "soy sauce", "Chilipulver": "chili powder", "Zucker": "sugar", "Ahornsirup": "maple syrup",
    "Vanilleextrakt": "vanilla extract", "Schokolade": "chocolate", "Backpulver": "baking powder", "Hefe": "yeast",
    "Senf": "mustard", "Melasse": "molasses", "Worcestersauce": "worcestershire sauce", "Miso-Paste": "miso paste",
    "Tahini": "tahini", "Kreuzkümmel": "cumin", "Thymian": "thyme", "Oregano": "oregano",
    "Rosmarin": "rosemary", "Basilikum": "basil", "Muskatnuss": "nutmeg", "Zimt": "cinnamon"
}


st.markdown("### 🔍 Suche starten")
search_button = st.button("🔎 Suchen")

diet = st.selectbox(
    "🧘 Diät wählen",
    ["Alle", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"],
)

# --- Vor der Anzeige der Rezepte: Hilfsfunktionen und forbidden_dict bereitstellen ---
forbidden_dict = {
    "Vegetarisch": [
        "chicken", "poulet", "rind", "rindfleisch", "beef", "schwein", "schweinefleisch", "pork", "speck", "bacon", "wurst", "salami", "lamm", "ente", "gans", "pute", "truthahn", "fisch", "thunfisch", "lachs", "shrimp", "garnelen", "krabben", "meeresfrüchte", "seafood"
    ],
    "Vegan": [
        "chicken", "poulet", "rind", "rindfleisch", "beef", "schwein", "schweinefleisch", "pork", "speck", "bacon", "wurst", "salami", "lamm", "ente", "gans", "pute", "truthahn", "fisch", "thunfisch", "lachs", "shrimp", "garnelen", "krabben", "meeresfrüchte", "seafood",
        "ei", "egg", "käse", "cheese", "milch", "milk", "joghurt", "yogurt", "butter", "quark", "sahne", "cream", "honig", "honey"
    ],
    "Kein Schweinefleisch": ["schwein", "schweinefleisch", "pork"],
    "Pescitarisch": [
        "chicken", "poulet", "rind", "rindfleisch", "beef", "schwein", "schweinefleisch", "pork", "speck", "bacon", "wurst", "salami", "lamm", "ente", "gans", "pute", "truthahn"
    ],
    "laktosefrei": [
        "milch", "milk", "käse", "cheese", "joghurt", "yogurt", "butter", "quark", "sahne", "cream", "kondensmilch", "frischkäse", "parmesan", "buttermilch"
    ]
}
def extract_ingredients(val):
    if isinstance(val, list):
        return [str(x).strip().lower() for x in val]
    try:
        parsed = ast.literal_eval(val)
        if isinstance(parsed, list):
            return [str(x).strip().lower() for x in parsed]
    except Exception:
        pass
    return [x.strip().lower() for x in re.split(r'[;,]', str(val)) if x.strip()]
def forbidden_in_ingredients(ingredient_val, forbidden_words):
    ingredients = extract_ingredients(ingredient_val)
    for ing in ingredients:
        for word in forbidden_words:
            if re.fullmatch(rf".*\\b{re.escape(word)}\\b.*", ing):
                return True
    return False
def forbidden_in_text(val, forbidden_words):
    val = str(val).lower()
    for word in forbidden_words:
        if re.search(rf"\\b{re.escape(word)}\\b", val):
            return True
    return False

if search_button:
    suchergebnisse = rezepte.copy()
    st.write(f"Vor Filter: {len(suchergebnisse)} Rezepte")

    forbidden = forbidden_dict.get(diet, [])
    if forbidden:
        # Remove recipes with forbidden ingredients
        before = len(suchergebnisse)
        suchergebnisse = suchergebnisse[~suchergebnisse['RecipeIngredientParts'].apply(lambda x: forbidden_in_ingredients(x, forbidden))]
        st.write(f"Nach Zutaten-Filter: {len(suchergebnisse)} Rezepte (entfernt: {before-len(suchergebnisse)})")
        # Remove recipes with forbidden in Name, Description, Keywords
        for col in ["Name", "Description", "Keywords"]:
            if col in suchergebnisse.columns:
                before = len(suchergebnisse)
                suchergebnisse = suchergebnisse[~suchergebnisse[col].apply(lambda x: forbidden_in_text(x, forbidden))]
                st.write(f"Nach {col}-Filter: {len(suchergebnisse)} Rezepte (entfernt: {before-len(suchergebnisse)})")

    # Nach Mahlzeittyp filtern
    if meal_type != "Alle":
        suchergebnisse = suchergebnisse[suchergebnisse['MealType'].str.contains(meal_type, case=False, na=False)]

    # Nach Zutaten filtern
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

    for _, row in suchergebnisse.head(20).iterrows():
        rezept_id = row.get("ID") or row.get("RecipeId")
        # Prüfe, ob das Rezept eigentlich verboten wäre (z.B. Fleisch bei Vegetarisch)
        highlight = False
        forbidden = forbidden_dict.get(diet, [])
        if forbidden:
            if forbidden_in_ingredients(row.get('RecipeIngredientParts', ''), forbidden):
                highlight = True
            for col in ["Name", "Description", "Keywords"]:
                if forbidden_in_text(row.get(col, ''), forbidden):
                    highlight = True
        row1, heart_col = st.columns([5, 1])
        with row1:
            if highlight:
                st.markdown(f"### <span style='color:red'>🍽️ {row['Name']}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"### 🍽️ {row['Name']}")
            st.write(f"**Kategorie:** {row.get('RecipeCategory', '-')} | **Mahlzeit:** {row.get('MealType', '-')} | **Kochzeit:** {row.get('CookTime', '-')}")
            with heart_col:
                if rezept_id in st.session_state.favoriten:
                    if st.button("💔", key=f"remove_{rezept_id}"):
                        st.session_state.favoriten.remove(rezept_id)
                        st.experimental_rerun()
                else:
                    if st.button("❤️", key=f"add_{rezept_id}"):
                        st.session_state.favoriten.append(rezept_id)
                        st.experimental_rerun()
                        
        # Bild anzeigen (unterhalb)
        raw_img = str(row.get("Images", "")).strip()
        url = None
        if raw_img.startswith("c("):
            try:
                url_list = ast.literal_eval(raw_img[1:])
                if url_list:
                    url = url_list[0]
            except Exception:
                pass
        elif raw_img.startswith("http"):
            url = raw_img
        if url:
            st.image(url, use_container_width=True)
        else:
            st.markdown("*(kein Bild)*")
        st.markdown("---")
                
        # Zubereitung (immer anzeigen!)
        instr_raw = str(row["RecipeInstructions"])
        step_list = instr_raw.strip('c()[]').replace('"', '').split('", "')
        if len(step_list) == 1:
            step_list = re.split(r'[.\n]\s+', instr_raw.strip('c()[]').replace('"', ''))
        st.markdown("**📝 Zubereitung:**")
        for idx, step in enumerate(step_list, start=1):
            if step.strip():
                st.markdown(f"{idx}. {step.strip()}")

# Einheitliche ID-Spalte
if "ID" not in rezepte.columns and "RecipeId" in rezepte.columns:
    rezepte["ID"] = rezepte["RecipeId"]

rezepte = st.session_state['data']






st.markdown("---")

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

