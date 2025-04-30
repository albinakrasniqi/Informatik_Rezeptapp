import streamlit as st
import pandas as pd

# Datensatz laden
@st.cache_data
def load_data():
    # Pfad zum Datensatz anpassen
    return pd.read_csv("path_to_your_dataset.csv")  # Ersetze mit dem tatsächlichen Pfad

df = load_data()

# Überprüfen, ob der Datensatz korrekt geladen wurde
if df.empty:
    st.error("Der Datensatz konnte nicht geladen werden. Bitte überprüfe den Pfad.")
    st.stop()

# Benutzeroberfläche
st.title("🍽️ Rezeptsuche")

# 🥗 Diätfilter
diet = st.selectbox("🧘 Diät wählen", ["Alle", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "Pescitarisch", "laktosefrei"])

# 🍲 Mahlzeittyp
meal_type = st.selectbox("🍽️ Mahlzeit", ["Alle", "Frühstück", "Mittagessen", "Abendessen", "Snack"])

# 🍎 Zutaten auswählen
ingredients = st.multiselect(
    "Wähle Zutaten:",
    ["Karotte", "Tomate", "Zwiebel", "Knoblauch", "Paprika", "Brokkoli", "Reis", "Spaghetti"]
)

# Rezept suchen Button
if st.button("Rezept suchen"):
    # Filterlogik
    filtered_df = df

    # Filter nach Diät
    if diet != "Alle":
        if "diet" in df.columns:
            filtered_df = filtered_df[filtered_df["diet"].str.contains(diet, case=False, na=False)]
        else:
            st.warning("Die Spalte 'diet' wurde im Datensatz nicht gefunden.")

    # Filter nach Mahlzeittyp
    if meal_type != "Alle":
        if "meal_type" in df.columns:
            filtered_df = filtered_df[filtered_df["meal_type"].str.contains(meal_type, case=False, na=False)]
        else:
            st.warning("Die Spalte 'meal_type' wurde im Datensatz nicht gefunden.")

    # Filter nach Zutaten
    if ingredients:
        if "ingredients" in df.columns:
            for ingredient in ingredients:
                filtered_df = filtered_df[filtered_df["ingredients"].str.contains(ingredient, case=False, na=False)]
        else:
            st.warning("Die Spalte 'ingredients' wurde im Datensatz nicht gefunden.")

    # Ergebnisse anzeigen
    if not filtered_df.empty:
        st.subheader("🔎 Gefundenes Rezept")
        st.write(filtered_df.iloc[0])  # Zeige das erste passende Rezept
    else:
        st.warning("Keine passenden Rezepte gefunden. Bitte passe deine Filter an.")