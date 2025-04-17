import pandas as pd
import json

# Emoji-Mapping
emoji_map = {
    "broccoli": "🥦",
    "carrot": "🥕",
    "salmon": "🐟",
    "chicken": "🍗",
    "rice": "🍚",
    "tomato": "🍅",
    "cheese": "🧀",
    "egg": "🥚",
    "beef": "🥩",
    "bread": "🍞"
}

def zutat_zu_emoji(zutat):
    for schlüsselwort, emoji in emoji_map.items():
        if schlüsselwort in zutat.lower():
            return emoji
    return "❓"

# CSV-Datei laden
df = pd.read_csv("full_dataset.csv")

# Beispiel: Nur die ersten 100 Rezepte verwenden
rezepte = []
for index, row in df.head(100).iterrows():
    zutaten_liste = json.loads(row['ingredients'])
    emojis = [zutat_zu_emoji(z) for z in zutaten_liste]
    rezepte.append({
        "titel": row['title'],
        "zutaten": emojis,
        "beschreibung": row['instructions'],
        "bild_url": row.get('image_url', '')
    })

# Als JSON speichern
with open("data/rezepte.json", "w", encoding="utf-8") as f:
    json.dump(rezepte, f, ensure_ascii=False, indent=2)
