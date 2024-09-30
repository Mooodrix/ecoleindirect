import csv

# Fichier où les données seront sauvegardées
FILENAME = 'etudiants.csv'

# Fonction pour initialiser le fichier avec les colonnes principales
def initialiser_fichier():
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Nom', 'Matière', 'Note'])

# Fonction pour ajouter un étudiant et sa note
def ajouter_etudiant(nom, matiere, note):
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nom, matiere, note])
    print(f"Étudiant {nom} ajouté avec une note de {note} en {matiere}.")

# Fonction pour afficher toutes les données des étudiants
def afficher_etudiants():
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Sauter l'en-tête
        for row in reader:
            print(f"Étudiant: {row[0]}, Matière: {row[1]}, Note: {row[2]}")

# Fonction pour calculer la moyenne des notes d'un étudiant
def calculer_moyenne(nom):
    total_notes = 0
    nombre_notes = 0
    with open(FILENAME, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Sauter l'en-tête
        for row in reader:
            if row[0] == nom:
                total_notes += float(row[2])
                nombre_notes += 1
    if nombre_notes > 0:
        moyenne = total_notes / nombre_notes
        print(f"La moyenne de {nom} est {moyenne:.2f}.")
    else:
        print(f"Aucune note trouvée pour {nom}.")

# Programme principal
def menu():
    while True:
        print("\nMenu :")
        print("1. Ajouter un étudiant")
        print("2. Afficher tous les étudiants")
        print("3. Calculer la moyenne d'un étudiant")
        print("4. Quitter")
        choix = input("Choisissez une option : ")

        if choix == '1':
            nom = input("Nom de l'étudiant : ")
            matiere = input("Matière : ")
            note = input("Note : ")
            ajouter_etudiant(nom, matiere, note)
        elif choix == '2':
            afficher_etudiants()
        elif choix == '3':
            nom = input("Nom de l'étudiant : ")
            calculer_moyenne(nom)
        elif choix == '4':
            print("Au revoir !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

# Initialisation du fichier et démarrage du programme
initialiser_fichier()
menu()
