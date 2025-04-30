import streamlit as st
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Kaggle-Datensatz herunterladen und laden
path = kagglehub.dataset_download("irkaal/foodcom-recipes-and-reviews")
print("Path to dataset files:", path)

# Set the path to the file you'd like to load
file_path = ""  # Falls der Datensatz lokal gespeichert ist, hier den Pfad angeben

# Datensatz laden
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "irkaal/foodcom-recipes-and-reviews",
    file_path,
)

# Überprüfen, ob der Datensatz korrekt geladen wurde
if df.empty:
    st.error("Der Datensatz konnte nicht geladen werden. Bitte überprüfe den Pfad oder die Kaggle-API.")
    st.stop()

# Spaltennamen überprüfen
print("Spalten im Datensatz:", df.columns)

# Streamlit App
st.title("Rezeptfilter")

# Benutzerpräferenzen über die Streamlit-Oberfläche
st.sidebar.header("Filteroptionen")
diet_option = st.sidebar.selectbox(
    "Wähle deine Diät:",
    ["Keine Einschränkung", "Vegetarisch", "Vegan", "Kein Schweinefleisch", "laktosefrei"]
)
ingredients_option = st.sidebar.multiselect(
    "Wähle Zutaten:",
    ["Karotte", "Tomate", "Zwiebel", "Knoblauch", "Paprika", "Brokkoli", "Reis", "Spaghetti"]
)

# Benutzerpräferenzen speichern
user_preferences = {
    "diät": None if diet_option == "Keine Einschränkung" else diet_option,
    "zutaten": ingredients_option,
}

def filter_recipes(dataframe, preferences):
    """
    Dynamische Filterfunktion für Rezepte basierend auf Benutzerpräferenzen.
    
    :param dataframe: Pandas DataFrame mit Rezeptdaten
    :param preferences: Dictionary mit Benutzerpräferenzen
    :return: Gefilterter DataFrame
    """
    filtered_df = dataframe

    # Filter nach Diät, falls angegeben
    if preferences["diät"]:
        if "diet" in dataframe.columns:
            filtered_df = filtered_df[filtered_df["diet"].str.contains(preferences["diät"], case=False, na=False)]
        else:
            st.warning("Die Spalte 'diet' wurde im Datensatz nicht gefunden.")

    # Filter nach Zutaten, falls angegeben
    if "ingredients" in dataframe.columns:
        for zutat in preferences["zutaten"]:
            filtered_df = filtered_df[filtered_df["ingredients"].str.contains(zutat, case=False, na=False)]
    else:
        st.warning("Die Spalte 'ingredients' wurde im Datensatz nicht gefunden.")

    return filtered_df

# "Suchen"-Button
if st.sidebar.button("Suchen"):
    # Filtere die Rezepte basierend auf den Benutzerpräferenzen
    filtered_recipes = filter_recipes(df, user_preferences)

    # Ergebnisse anzeigen
    st.header("Gefilterte Rezepte")
    if not filtered_recipes.empty:
        st.write(filtered_recipes.head())  # Zeige die ersten 5 passenden Rezepte
    else:
        st.warning("Keine passenden Rezepte gefunden. Bitte passe deine Filter an.")
        