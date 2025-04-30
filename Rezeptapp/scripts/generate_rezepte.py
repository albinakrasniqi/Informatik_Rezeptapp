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

# Funktion zur Filterung der Rezepte
def filter_recipes(dataframe, diet, ingredients, meal_type):
    """
    Filtert Rezepte basierend auf Diät, Zutaten und Mahlzeittyp.
    
    :param dataframe: Pandas DataFrame mit Rezeptdaten
    :param diet: Ausgewählte Diät (z. B. "Vegetarisch", "Vegan")
    :param ingredients: Liste der ausgewählten Zutaten
    :param meal_type: Ausgewählter Mahlzeittyp (z. B. "Frühstück", "Mittagessen")
    :return: Gefilterter DataFrame
    """
    filtered_df = dataframe

    # Filter nach Diät
    if diet and diet != "Alle":
        if "diet" in dataframe.columns:
            filtered_df = filtered_df[filtered_df["diet"].str.contains(diet, case=False, na=False)]
        else:
            st.warning("Die Spalte 'diet' wurde im Datensatz nicht gefunden.")

    # Filter nach Zutaten
    if ingredients and "ingredients" in dataframe.columns:
        for ingredient in ingredients:
            filtered_df = filtered_df[filtered_df["ingredients"].str.contains(ingredient, case=False, na=False)]
    elif "ingredients" not in dataframe.columns:
        st.warning("Die Spalte 'ingredients' wurde im Datensatz nicht gefunden.")

    # Filter nach Mahlzeittyp
    if meal_type and meal_type != "Alle":
        if "meal_type" in dataframe.columns:
            filtered_df = filtered_df[filtered_df["meal_type"].str.contains(meal_type, case=False, na=False)]
        else:
            st.warning("Die Spalte 'meal_type' wurde im Datensatz nicht gefunden.")

    return filtered_df

# Funktion, um die gefilterten Rezepte anzuzeigen
def get_filtered_recipes(diet, ingredients, meal_type):
    filtered_recipes = filter_recipes(df, diet, ingredients, meal_type)
    if not filtered_recipes.empty:
        return filtered_recipes.head(1)  # Zeige das erste passende Rezept
    else:
        return None 