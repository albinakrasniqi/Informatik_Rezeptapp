import pandas as pd

# Funktion, um ein Rezept basierend auf Benutzereingaben zu finden
def finde_rezept(angaben):
    # Datensatz laden (z.B. als CSV-Datei)
    datensatz = pd.read_csv('c:/Users/arifi/OneDrive - ZHAW/2. Semester/Informatik/Eigene App/Datensatz/rezeptdaten.csv')

    # Filtere den Datensatz basierend auf den Angaben
    gefundene_rezepte = datensatz
    for schluessel, wert in angaben.items():
        gefundene_rezepte = gefundene_rezepte[gefundene_rezepte[schluessel] == wert]

    # Überprüfen, ob ein Rezept gefunden wurde
    if not gefundene_rezepte.empty:
        return gefundene_rezepte
    else:
        return "Kein passendes Rezept gefunden."

# Benutzerangaben abfragen
def benutzereingaben_abfragen():
    print("Bitte geben Sie die folgenden Angaben ein:")
    zutat = input("Zutat: ")
    schwierigkeit = input("Schwierigkeit (z. B. Einfach, Mittel, Schwer): ")
    dauer = input("Dauer (z. B. 30 Minuten): ")

    return {
        'Zutat': zutat,
        'Schwierigkeit': schwierigkeit,
        'Dauer': dauer
    }

# Hauptprogramm
if __name__ == "__main__":
    angaben = benutzereingaben_abfragen()
    ergebnis = finde_rezept(angaben)
    print("\nSuchergebnis:")
    print(ergebnis)


