import pandas as pd
import json

# Emoji-Mapping
emoji_map = {
    "broccoli": "🥦",
    "carrot": "🥕",
    "salmon": "🐟",
    "chicken": "🍗",
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

# 📄 CSV-Datei laden (jetzt die kleine!)
df = pd.read_csv("Rezeptapp/scripts/dataset/klein_dataset.csv")

# 🧪 Nur die ersten 100 Rezepte verwenden (optional – du hast eh 100)
rezepte = []
for index, row in df.iterrows():
    zutaten_liste = json.loads(row['ingredients'])
    emojis = [zutat_zu_emoji(z) for z in zutaten_liste]
    rezepte.append({
        "titel": row['title'],
        "zutaten": emojis,
        "beschreibung": row['instructions'],
        "bild_url": row.get('image_url', '')
    })

# 💾 Als JSON speichern
with open("Rezeptapp/data/rezepte.json", "w", encoding="utf-8") as f:
    json.dump(rezepte, f, ensure_ascii=False, indent=2)

print("✅ Rezepte erfolgreich generiert!")

