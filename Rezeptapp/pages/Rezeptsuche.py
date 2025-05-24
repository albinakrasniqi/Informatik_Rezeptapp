import streamlit as st
import pandas as pd
import uuid  # Für die Generierung von IDs
from utils.data_manager import DataManager  # Falls benötigt, sicherstellen, dass utils verfügbar ist
import re
import ast
import csv
import io
import requests
from requests.auth import HTTPBasicAuth


data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Rezeptapp2")

suchergebnisse = pd.DataFrame()  # leeres DataFrame zur Initialisierung

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

# Rezepte DataFrame aus Session State laden
rezepte = st.session_state['data']


# Falls leer, sofort stoppen
if rezepte.empty:
    st.error("❌ Keine Daten im Rezept-Datensatz! Bitte prüfe die Datei in SwitchDrive.")
    st.stop()

# Zutaten-Emoji-Gruppen definieren
zutat_emojis_gruppen = {
    "Kohlenhydrate & Getreide": {
        "🍞": "Brot", "🥖": "Baguette", "🥨": "Brezel", "🍚": "Reis", "🍜": "Nudeln",
        "🫓": "Fladenbrot", "🌽": "Mais", "🍝": "Pasta", "🟫": "Quinoa", "🍢": "Couscous",
        "🥣": "Hirse", "🍥": "Polenta", "🧇": "Haferflocken", "🥯": "Bagel", "🥞": "Pfannkuchen",
        "🌾": "Mehl"
    },
    "Gemüse": {
        "🥦": "Brokkoli", "🥕": "Karotte", "🌶": "Paprika", "🍆": "Aubergine", "🧄": "Knoblauch",
        "🧅": "Zwiebel", "🍄": "Pilze", "🥒": "Gurke", "🍅": "Tomate",
        "🫑": "Peperoni", "🥗": "Salat", "🥔": "Kartoffel", "🍠": "Süßkartoffel", "🪴": "Spinat",
        "🎃": "Kürbis", "🥒 + 🟢": "Zucchini", "🥬": "Kohl", "🫛": "Sellerie"
    },
    "Obst": {
        "🍎": "Apfel", "🍐": "Birne", "🍊": "Orange", "🍋": "Zitrone", "🍌": "Banane",
        "🍉": "Wassermelone", "🍇": "Trauben", "🍓": "Erdbeere", "🫐": "Blaubeeren",
        "🥭": "Mango", "🍍": "Ananas", "🥝": "Kiwi", "🍒": "Kirsche", "🍑": "Pfirsich"
    },
    "Eiweissquellen": {
        "🍗": "Poulet", "🥩": "Rindfleisch", "🍖": "Schweinefleisch", "🐟": "Fisch",
        "🦐": "Garnelen", "🥚": "Ei", "🍳": "Eiweiss", "🥓": "Speck",
        "🧆": "Falafel", "🍶": "Quark", "🥣": "Joghurt", "🌭": "Wurst"
    },
    "Hülsenfrüchte & Nüsse": {
        "🥜": "Erdnüsse", "🫘": "Bohnen", "🟤": "Linsen",
        "🟡": "Gelbe Linsen", "🟣": "Schwarze Bohnen", "🟢": "Kichererbsen",
        "🔴": "Rote Linsen", "⚪": "Weiße Bohnen", "💚": "Grüne Erbsen",
        "🌸🌰": "Mandeln", "🌰": "Walnüsse", "🥥": "Kokosnuss"
    },
    "Milchprodukte & Alternativen": {
        "🥛": "Milch", "🧈": "Butter", "🧀": "Käse", "🥥🥛": "Kokosmilch",
        "🌱": "Sojamilch", "☁️": "Sahne", "🥯": "Frischkäse",
        "🧴": "Kondensmilch"
    },
    "Extras": {
        "🧂": "Salz", "🫒": "Olivenöl", "🍯": "Honig", "🧃": "Essig", "🥫": "Tomatenmark",
        "🫙": "Sojasauce", "🌶": "Chilipulver", "🍬": "Zucker", "🍁": "Ahornsirup",
        "🧁": "Vanilleextrakt", "🍫": "Schokolade", "🍩": "Backpulver", "🥄": "Senf", "🌿": "Basilikum", "🪵": "Zimt"
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
            key = f"{gruppe}_{emoji}"

            # Toggle-Auswahl über Checkbox
            checked = st.session_state.auswahl and emoji in st.session_state.auswahl
            checkbox = cols[j].checkbox(label, value=checked, key=key)

            if checkbox and emoji not in st.session_state.auswahl:
                st.session_state.auswahl.append(emoji)
            elif not checkbox and emoji in st.session_state.auswahl:
                st.session_state.auswahl.remove(emoji)

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

# Diätform anzeigen 
gespeicherte_diät = st.session_state.get("gespeicherte_diätform", "Alle")
st.markdown(f"### 🧘 Ausgewählte Diät: {gespeicherte_diät}")

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
    "Garnelen": "shrimp", "Ei": "egg", "Eiweiss": "egg white", "Speck": "bacon",
    "Falafel": "falafel", "Thunfisch": "tuna", "Quark": "quark", "Joghurt": "yogurt",
    "Wurst": "sausage",

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

# Such feld
st.markdown("### 🔍 Suche starten")
search_button = st.button("🔎 Suchen")

#forbidden_dict/ diätformen codiert
forbidden_dict = {
    "Vegetarisch": [
        "chicken", "chicken broth", "broth", "bouillon", "poulet",
        "rind", "rindfleisch", "beef",
        "schwein", "schweinefleisch", "pork",
        "speck", "bacon", "wurst", "salami",
        "lamm", "ente", "gans", "pute", "truthahn",
        "fisch", "thunfisch", "lachs", "shrimp", "garnelen", "krabben", "meeresfrüchte", "seafood",
        "ham", "schinken"
    ],
    "Vegan": [
        "chicken", "chicken broth", "broth", "bouillon", "poulet",
        "rind", "rindfleisch", "beef",
        "schwein", "schweinefleisch", "pork",
        "speck", "bacon", "wurst", "salami",
        "lamm", "ente", "gans", "pute", "truthahn",
        "fisch", "thunfisch", "lachs", "shrimp", "garnelen", "krabben", "meeresfrüchte", "seafood",
        "ham", "schinken",
        "ei", "egg", "käse", "cheese", "milch", "milk", "joghurt", "yogurt", "butter", "quark", "sahne", "cream", "honig", "honey"
    ],
    "Kein Schweinefleisch": ["schwein", "schweinefleisch", "pork", "speck", "bacon", "wurst", "salami", "ham", "schinken"],
    "Pescitarisch": [
        "chicken", "chicken broth", "broth", "bouillon", "poulet",
        "rind", "rindfleisch", "beef",
        "schwein", "schweinefleisch", "pork",
        "speck", "bacon", "wurst", "salami",
        "lamm", "ente", "gans", "pute", "truthahn",
        "ham", "schinken"
    ],
    "laktosefrei": [
        "milch", "milk", "käse", "cheese", "joghurt", "yogurt", "butter", "quark", "sahne", "cream", "kondensmilch", "frischkäse", "parmesan", "buttermilch"
    ]
}
def extract_ingredients(val):
    # Handles R-style c("...") and Python list/str
    if isinstance(val, list):
        return [str(x).strip().lower() for x in val]
    s = str(val).strip().lower()
    if s.startswith('c(') and s.endswith(')'):
        # Remove c( and ) and split by comma
        s = s[2:-1]
        # Remove quotes and split
        items = [x.strip().strip('"\'') for x in s.split(',')]
        return [x for x in items if x]
    try:
        parsed = ast.literal_eval(val)
        if isinstance(parsed, list):
            return [str(x).strip().lower() for x in parsed]
    except Exception:
        pass
    # fallback: split by comma/semicolon
    return [x.strip().lower() for x in re.split(r'[;,]', s) if x.strip()]
def forbidden_in_ingredients(ingredient_val, forbidden_words):
    ingredients = extract_ingredients(ingredient_val)
    # Zutaten-Namen extrahieren (z.B. "🍗 Poulet" -> "Poulet")
    zutaten_namen = []
    for ing in ingredients:
        # Emoji entfernen, falls vorhanden
        name = ing
        if " " in ing:
            name = ing.split(" ", 1)[1]
        zutaten_namen.append(name.lower())
    # Übersetze ins Englische
    zutaten_englisch = [deutsch_to_englisch.get(name.capitalize(), name.lower()) for name in zutaten_namen]
    # Prüfe auf verbotene Zutaten
    for zutat in zutaten_englisch:
        for word in forbidden_words:
            if re.search(rf"\b{re.escape(word)}\b", zutat):
                return True
    return False

def format_ingredients(val):
    items = extract_ingredients(val)
    return ", ".join(items)

if search_button:
    suchergebnisse = rezepte.copy()
    st.write(f"Vor Filter: {len(suchergebnisse)} Rezepte")

    diet = st.session_state.get("gespeicherte_diätform", "Alle")
    forbidden = forbidden_dict.get(diet, [])

    def has_forbidden(row):
        if forbidden_in_ingredients(row.get('RecipeIngredientParts', ''), forbidden):
            return True
        for col in ["Name", "Description", "Keywords"]:
            if forbidden_in_text(row.get(col, ''), forbidden):
                return True
        return False

    suchergebnisse['forbidden'] = suchergebnisse.apply(has_forbidden, axis=1)

    selected_ingredient_names = [
        deutsch_to_englisch.get(name, name)
        for gruppe in zutat_emojis_gruppen.values()
        for emoji, name in gruppe.items()
        if emoji in st.session_state.auswahl
    ]

    if selected_ingredient_names:
        suchergebnisse = suchergebnisse[
            suchergebnisse['RecipeIngredientParts'].astype(str).apply(
                lambda x: all(z in x for z in selected_ingredient_names)
            )
        ]

    if suchergebnisse.empty:
        st.warning("❌ Kein passendes Rezept gefunden.")
        st.session_state['suchergebnisse'] = pd.DataFrame()  # Leeren
    else:
        st.success(f"✅ {len(suchergebnisse)} Rezept(e) gefunden.")
        st.session_state['suchergebnisse'] = suchergebnisse

def toggle_favorit(rezept_id):
    if rezept_id in st.session_state.favoriten:
        st.session_state.favoriten.remove(rezept_id)
    else:
        st.session_state.favoriten.append(rezept_id)

# 🔄 Rezepte anzeigen, wenn vorhanden
def zeige_rezept(row, idx):
    import ast
    import re

    rezept_id = row.get("ID") or row.get("RecipeId")
    row1, heart_col = st.columns([5, 1])
    with row1:
        # Titel rot markieren, wenn forbidden
        if row.get('forbidden', False):
            st.markdown(f"### <span style='color:red'>🍽️ {row['Name']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"### 🍽️ {row['Name']}")
        st.write(f"**Kategorie:** {row.get('RecipeCategory', '-')} | **Kochzeit:** {row.get('CookTime', '-')}" )
        formatted_ingredients = format_ingredients(row.get('RecipeIngredientParts', ''))
        st.write(f"**Zutaten:** {formatted_ingredients}")

    # Favoriten-Button
    col1, heart_col = st.columns([8, 1])
    with heart_col:
        is_fav = rezept_id in st.session_state.favoriten
        icon = "❤️" if is_fav else "🤍"
        if st.button(icon, key=f"fav_{rezept_id}_{idx}"):
            if is_fav:
                st.session_state.favoriten.remove(rezept_id)
            else:
                st.session_state.favoriten.append(rezept_id)
            st.rerun()

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

    # Zutaten anzeigen
    def extract_ingredients(val):
        import re
        if isinstance(val, list):
            return [str(x).strip().lower() for x in val]
        s = str(val).strip().lower()
        if s.startswith('c(') and s.endswith(')'):
            s = s[2:-1]
            items = [x.strip().strip('"\'') for x in s.split(',')]
            return [x for x in items if x]
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, list):
                return [str(x).strip().lower() for x in parsed]
        except Exception:
            pass
        return [x.strip().lower() for x in re.split(r'[;,]', s) if x.strip()]

    # Zutaten + Mengen formatieren
    parts = extract_ingredients(row.get("RecipeIngredientParts", ""))
    mengen = extract_ingredients(row.get("RecipeIngredientQuantities", ""))

    st.markdown("**🧾 Zutaten mit Mengen:**")
    for i, zutat in enumerate(parts):
        menge = mengen[i] if i < len(mengen) else ""
        st.markdown(f"- {menge} {zutat}".strip())

    # Zubereitung (immer anzeigen!)
    instr_raw = str(row["RecipeInstructions"])
    step_list = instr_raw.strip('c()[]').replace('"', '').split('", "')
    if len(step_list) == 1:
        step_list = re.split(r'[.\n]\s+', instr_raw.strip('c()[]').replace('"', ''))
    st.markdown("**📝 Zubereitung:**")
    for step_idx, step in enumerate(step_list, start=1):
        if step.strip():
            st.markdown(f"{step_idx}. {step.strip()}") 

    # (Entfernt: Doppelte Anzeige und Favoriten-Logik, da dies bereits oben erledigt wird)


# ...existing code...

if 'suchergebnisse' in st.session_state and not st.session_state['suchergebnisse'].empty:
    for idx, row in st.session_state['suchergebnisse'].iterrows():
        zeige_rezept(row, idx)

# ...existing code...


# Einheitliche ID-Spalte
if "ID" not in rezepte.columns and "RecipeId" in rezepte.columns:
    rezepte["ID"] = rezepte["RecipeId"]

rezepte = st.session_state['data']

if "gespeicherte_diätform" in st.session_state and "diätform" not in st.session_state:
    st.session_state["diätform"] = st.session_state["gespeicherte_diätform"]


#Rezept hinzufügen
import datetime

def Rezept_speichern(username, rezepte_liste):
    # WebDAV-Zugangsdaten aus st.secrets oder deiner Konfiguration
    base_url = st.secrets["webdav"]["base_url"]
    webdav_user = st.secrets["webdav"]["username"]
    webdav_password = st.secrets["webdav"]["password"]

    # Zielpfad für die Rezepte-Datei auf WebDAV
    url = f"{base_url}/files/{webdav_user}/rezepte_{username}.csv"
    auth = HTTPBasicAuth(webdav_user, webdav_password)
    output = io.StringIO()
    # Feldnamen anpassen, falls du weitere Felder hast
    fieldnames = rezepte_liste[0].keys() if rezepte_liste else ["Name", "RecipeIngredientParts", "RecipeInstructions", "ID", "DateAdded"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rezepte_liste)
    try:
        response = requests.put(
            url,
            data=output.getvalue().encode("utf-8"),
            headers={"Content-Type": "text/csv"},
            auth=auth
        )
        if response.status_code not in [200, 201, 204]:
            st.error(f"Speichern auf WebDAV fehlgeschlagen: {response.status_code}")
    except Exception as e:
        st.error(f"WebDAV-Speicherfehler: {e}")

if st.button("➕ Eigenes Rezept hinzufügen"):
    with st.form("rezept_hinzufuegen_formular"):
        rezept_name = st.text_input("📖 Rezepttitel eingeben")
        bild_url = st.text_input("📸 Bild-URL eingeben")
        diät = st.selectbox("🧘 Diät", ["Vegetarisch", "Vegan", "Kein Schweinefleisch"])
        zutaten_emojis = st.multiselect(
            "Zutaten auswählen",
            [f"{emoji} {name}" for gruppe in zutat_emojis_gruppen.values() for emoji, name in gruppe.items()]
        )
        zutaten_mit_mengen = st.text_area("Zutaten mit Mengenangaben")
        anleitung = st.text_area("📝 Schritt-für-Schritt Anleitung")
        abgesendet = st.form_submit_button("✅ Rezept speichern")

        if abgesendet:
            # Zutaten-Check: mindestens eine Zutat ausgewählt oder Mengenangaben gemacht
            if not rezept_name or (not zutaten_emojis and not zutaten_mit_mengen) or not anleitung:
                st.error("Bitte mindestens einen Titel, Zutaten und eine Anleitung angeben.")
            else:
                new_recipe = {
                    "Name": rezept_name,
                    "Images": bild_url,
                    "RecipeCategory": diät,
                    "RecipeIngredientParts": zutaten_emojis,
                    "RecipeIngredientQuantities": zutaten_mit_mengen,
                    "RecipeInstructions": anleitung,
                    "ID": str(uuid.uuid4()),
                    "DateAdded": datetime.datetime.now().isoformat()
                }
                # Zum DataFrame hinzufügen
                if 'data' not in st.session_state or st.session_state['data'].empty:
                    st.session_state['data'] = pd.DataFrame([new_recipe])
                else:
                    st.session_state['data'] = pd.concat(
                        [st.session_state['data'], pd.DataFrame([new_recipe])],
                        ignore_index=True
                    )
                username = st.session_state.get("username", "user")
               
                # Lokale Speicherung:
                st.session_state['data'].to_csv(f"rezepte_{username}.csv", index=False)
                # WebDAV-Speicherung
                Rezept_speichern(username, st.session_state['data'].to_dict(orient="records"))
                st.success("✅ Rezept erfolgreich gespeichert! Du findest es unter 'Mein Konto'.")
