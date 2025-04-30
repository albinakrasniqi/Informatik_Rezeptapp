import streamlit as st
import pandas as pd

# Datensatz laden
@st.cache_data
def load_data():
    # Gib hier den korrekten Pfad zum Datensatz an
    return pd.read_csv("c:/Users/arifi/OneDrive - ZHAW/2. Semester/Informatik/Eigene App/Informatik_Rezeptapp/dataset.csv")

df = load_data()

# Überprüfen, ob der Datensatz korrekt geladen wurde
if df.empty:
    st.error("Der Datensatz konnte nicht geladen werden. Bitte überprüfe den Pfad.")
    st.stop()

# Benutzeroberfläche
st.title("🍽️ Gefundenes Rezept")

# Filterlogik basierend auf den Angaben von "Rezeptsuche.py"
# Die Angaben werden über `st.session_state` übergeben
diet = st.session_state.get("diet", "Alle")
meal_type = st.session_state.get("meal_type", "Alle")
ingredients = st.session_state.get("ingredients", [])

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



    st.session_state["diet"] = diet
st.session_state["meal_type"] = meal_type
st.session_state["ingredients"] = ingredients


print(df.columns)


st.session_state["diet"] = diet
st.session_state["meal_type"] = meal_type
st.session_state["ingredients"] = ingredients
st.experimental_rerun()  # Navigiere zur Seite "zRezeptangabe.py"


