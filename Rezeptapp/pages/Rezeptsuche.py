import streamlit as st
from utils.data_manager import DataManager


# initialize the data manager
data_manager = DataManager(fs_protocol='webdav', fs_root_folder="Rezeptapp2")  # switch drive 


if 'data' not in st.session_state:
    st.warning("📛 Keine Rezeptdaten gefunden. Bitte öffne zuerst die Startseite.")
    st.stop()



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
    zutaten = st.session_state.get('auswahl', [])

    if rezepte is None or rezepte.empty:
        st.error("⚠️ Keine Rezepte geladen.")
        st.stop()

    # Nur relevante Spalten auswählen
    relevante_spalten = [
        "Name", "CookTime", "PrepTime", "TotalTime", "Description", "Images",
        "RecipeCategory", "Keywords", "RecipeIngredientQuantities",
        "RecipeIngredientParts", "RecipeServings", "RecipeInstructions"
    ]
    vorhandene_spalten = [s for s in relevante_spalten if s in rezepte.columns]
    rezepte = rezepte[vorhandene_spalten]

    # Filtern nach ausgewählten Emojis
    if 'RecipeIngredientParts' in rezepte.columns:
        rezepte = rezepte[rezepte['RecipeIngredientParts'].apply(
            lambda z: any(zutat in str(z) for zutat in zutaten)
        )]

    # Filter nach Diät
    if diet != "Alle" and "RecipeCategory" in rezepte.columns:
        rezepte = rezepte[rezepte["RecipeCategory"] == diet]

    # Filter nach Mahlzeit
    if meal_type != "Alle" and "MealType" in rezepte.columns:
        rezepte = rezepte[rezepte["MealType"] == meal_type]

    # Ergebnisse anzeigen
    if rezepte.empty:
        st.warning("❌ Kein passendes Rezept gefunden.")
    else:
        st.success(f"✅ {len(rezepte)} Rezept(e) gefunden")
        for _, row in rezepte.iterrows():
            with st.container():
                if "Images" in row and pd.notna(row["Images"]):
                    st.image(row["Images"], width=300)
                st.markdown(f"### {row.get('Name', 'Ohne Titel')}")
                st.write(f"🕒 Gesamtzeit: {row.get('TotalTime', 'n/a')}")
                st.write(f"📝 Beschreibung: {row.get('Description', '')}")
                st.write(f"🥣 Zutaten: {row.get('RecipeIngredientParts', '')}")
                st.write(f"📏 Mengen: {row.get('RecipeIngredientQuantities', '')}")
                st.write(f"👨‍🍳 Anleitung: {row.get('RecipeInstructions', '')}")
