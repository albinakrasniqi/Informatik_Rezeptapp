import streamlit as st

def show():
    st.title("🍽️ Rezeptsuche")

    # 🔍 Suchleiste
    search_term = st.text_input("🔍 Suche nach einem Rezept:")
    if search_term:
        st.markdown(f"### 🔍 Suchergebnis für: {search_term}")

    # 🧩 Emoji-Filter
    st.markdown("### 🍎 Zutaten auswählen")

zutat_emojis = {
    # 🍞 Getreide & Kohlenhydrate
    "🍞": "Brot", "🥖": "Baguette", "🥐": "Croissant", "🥨": "Brezel",
    "🍚": "Reis", "🍙": "Reisbällchen", "🍘": "Reiscracker", "🍜": "Nudelsuppe",
    "🍝": "Spaghetti", "🥯": "Bagel", "🥞": "Pfannkuchen", "🧇": "Waffeln", "🫓": "Fladenbrot",

    # 🥦 Gemüse
    "🥦": "Brokkoli", "🥕": "Karotte", "🌽": "Mais", "🫑": "Paprika", "🍆": "Aubergine",
    "🥬": "Blattgemüse", "🥒": "Gurke", "🧄": "Knoblauch", "🧅": "Zwiebel", "🍄": "Pilze", "🍅": "Tomate", "🥗": "Gemischter Salat",

    # 🍎 Obst
    "🍎": "Apfel", "🍏": "Grüner Apfel", "🍐": "Birne", "🍊": "Orange", "🍋": "Zitrone",
    "🍌": "Banane", "🍉": "Wassermelone", "🍇": "Trauben", "🍓": "Erdbeere",
    "🫐": "Blaubeeren", "🥭": "Mango", "🍍": "Ananas", "🥝": "Kiwi",

    # 🥩 Eiweißquellen
    "🥩": "Steak", "🍗": "Hähnchenkeule", "🍖": "Rippchen", "🥓": "Speck", "🦴": "Knochen",
    "🐟": "Fisch", "🦐": "Garnelen", "🦑": "Tintenfisch", "🦞": "Hummer", "🥚": "Ei", "🍳": "Spiegelei", "🌭": "Wurst",

    # 🧀 Milchprodukte & Alternativen
    "🧀": "Käse", "🥛": "Milch", "🍶": "Reismilch/Sake", "🧈": "Butter", "🍨": "Eiscreme",
    "🍦": "Soft-Eis", "🥤": "Milchshake",

    # 🥜 Hülsenfrüchte & Nüsse
    "🥜": "Erdnüsse", "🌰": "Kastanien", "🫘": "Bohnen", "🍠": "Süßkartoffel",

    # 🍬 Extras
    "🧂": "Salz", "🫒": "Olive/Öl", "🧊": "Eiswürfel", "🍫": "Schokolade", "🍯": "Honig",
    "🍪": "Keks", "🍰": "Kuchen", "🍮": "Pudding"
    }

selected_ingredients = st.multiselect("Was hast du zu Hause?", zutat_emojis)

    # Display selected ingredients
if selected_ingredients:
        st.markdown("### 🛒 Ausgewählte Zutaten")
        st.write(", ".join(selected_ingredients))
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

