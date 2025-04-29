# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = ""

# Load the latest version
df = kagglehub.load_dataset(
  KaggleDatasetAdapter.PANDAS,
  "irkaal/foodcom-recipes-and-reviews",
  file_path,
  # Provide any additional arguments like 
  # sql_query or pandas_kwargs. See the 
  # documenation for more information:
  # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)

print("First 5 records:", df.head())



# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

# Set the path to the file you'd like to load
file_path = ""

# Load the latest version
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "irkaal/foodcom-recipes-and-reviews",
    file_path,
    # Provide any additional arguments like 
    # sql_query or pandas_kwargs. See the 
    # documenation for more information:
    # https://github.com/Kaggle/kagglehub/blob/main/README.md#kaggledatasetadapterpandas
)

# Dynamische Benutzerpräferenzen
user_preferences = {
    "diät": None,  # Optionen: Vegetarisch, Vegan, Kein Schweinefleisch, laktosefrei, etc. (None = keine Einschränkung)
    "zutaten": [],  # Liste von gewünschten Zutaten (z. B. ["Karotte", "Tomate"])
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
        filtered_df = filtered_df[filtered_df["diet"].str.contains(preferences["diät"], case=False, na=False)]

    # Filter nach Zutaten, falls angegeben
    for zutat in preferences["zutaten"]:
        filtered_df = filtered_df[filtered_df["ingredients"].str.contains(zutat, case=False, na=False)]

    return filtered_df

# Beispiel: Benutzer wählt "laktosefrei" und "Karotte"
user_preferences["diät"] = "laktosefrei"
user_preferences["zutaten"] = ["Karotte"]

# Filtere die Rezepte basierend auf den Benutzerpräferenzen
filtered_recipes = filter_recipes(df, user_preferences)

# Überprüfen, ob passende Rezepte gefunden wurden
if not filtered_recipes.empty:
    print("Gefilterte Rezepte:")
    print(filtered_recipes.head())
else:
    print("Keine passenden Rezepte gefunden. Bitte passe deine Filter an.")

