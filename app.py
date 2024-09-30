from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os

# Initialisation de Flask
app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Fichier CSV pour stocker les étudiants
FILENAME = 'etudiants.csv'

# Fonction pour initialiser le fichier avec les colonnes principales
def initialiser_fichier():
    if not os.path.exists(FILENAME):
        with open(FILENAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nom', 'Matière', 'Note'])

# Fonction pour ajouter un étudiant et sa note
def ajouter_etudiant(nom, matiere, note):
    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nom, matiere, note])

# Fonction pour lire tous les étudiants
def lire_etudiants():
    etudiants = []
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                etudiants.append({'Nom': row[0], 'Matière': row[1], 'Note': row[2]})
    return etudiants

# Fonction pour calculer la moyenne d'un étudiant
def calculer_moyenne(nom):
    total_notes = 0
    nombre_notes = 0
    if os.path.exists(FILENAME):
        with open(FILENAME, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                if row[0] == nom:
                    total_notes += float(row[2])
                    nombre_notes += 1
    if nombre_notes > 0:
        return total_notes / nombre_notes
    return None

# Route pour la page d'accueil
@app.route('/')
def index():
    etudiants = lire_etudiants()
    return render_template('index.html', etudiants=etudiants)

# Route pour ajouter un étudiant (formulaire)
@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        nom = request.form['nom']
        matiere = request.form['matiere']
        note = request.form['note']
        if nom and matiere and note:
            ajouter_etudiant(nom, matiere, note)
            flash(f"Étudiant {nom} ajouté avec succès.")
            return redirect(url_for('index'))
        else:
            flash("Tous les champs sont obligatoires.")
    return render_template('ajouter.html')

# Route pour calculer la moyenne d'un étudiant
@app.route('/moyenne', methods=['GET', 'POST'])
def moyenne():
    if request.method == 'POST':
        nom = request.form['nom']
        moyenne = calculer_moyenne(nom)
        if moyenne is not None:
            flash(f"La moyenne de {nom} est {moyenne:.2f}.")
        else:
            flash(f"Aucune note trouvée pour {nom}.")
        return redirect(url_for('index'))
    return render_template('moyenne.html')

# Initialisation du fichier
initialiser_fichier()

# Démarrage de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
