from flask import Flask, render_template, request, redirect, url_for, flash, session
import csv
import os
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

# Initialisation de Flask
app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Initialisation de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Fichiers CSV pour stocker les étudiants, professeurs et utilisateurs
FILENAME_ETUDIANTS = 'etudiants.csv'
FILENAME_PROFESSEURS = 'professeurs.csv'
FILENAME_UTILISATEURS = 'utilisateurs.csv'
FILENAME_MATIERES = 'matieres.csv'

# Fonction pour initialiser les fichiers
def initialiser_fichiers():
    if not os.path.exists(FILENAME_ETUDIANTS):
        with open(FILENAME_ETUDIANTS, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nom', 'Matière', 'Note'])
    if not os.path.exists(FILENAME_PROFESSEURS):
        with open(FILENAME_PROFESSEURS, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nom', 'Matière'])
    if not os.path.exists(FILENAME_UTILISATEURS):
        with open(FILENAME_UTILISATEURS, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Nom', 'Mot de passe', 'Role'])  # Role: 'etudiant' ou 'professeur'

# Modèle d'utilisateur
class User(UserMixin):
    def __init__(self, id, nom, role):
        self.id = id
        self.nom = nom
        self.role = role

# Fonction pour charger un utilisateur
@login_manager.user_loader
def load_user(user_id):
    if os.path.exists(FILENAME_UTILISATEURS):
        with open(FILENAME_UTILISATEURS, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                if row[0] == user_id:
                    return User(user_id, row[0], row[2])  # row[2] est le rôle
    return None

# Fonction pour ajouter un étudiant et sa note
def ajouter_etudiant(nom, matiere, note):
    with open(FILENAME_ETUDIANTS, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nom, matiere, note])

# Fonction pour lire tous les étudiants
def lire_etudiants():
    etudiants = []
    if os.path.exists(FILENAME_ETUDIANTS):
        with open(FILENAME_ETUDIANTS, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                etudiants.append({'Nom': row[0], 'Matière': row[1], 'Note': row[2]})
    return etudiants

# Fonction pour ajouter un professeur
def ajouter_professeur(nom, matiere):
    with open(FILENAME_PROFESSEURS, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nom, matiere])

# Fonction pour lire tous les professeurs
def lire_professeurs():
    professeurs = []
    if os.path.exists(FILENAME_PROFESSEURS):
        with open(FILENAME_PROFESSEURS, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                professeurs.append({'Nom': row[0], 'Matière': row[1]})
    return professeurs

# Fonction pour calculer la moyenne d'un étudiant
def calculer_moyenne(nom):
    total_notes = 0
    nombre_notes = 0
    if os.path.exists(FILENAME_ETUDIANTS):
        with open(FILENAME_ETUDIANTS, mode='r') as file:
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
    professeurs = lire_professeurs()
    return render_template('index.html', etudiants=etudiants, professeurs=professeurs)

# Route pour ajouter un étudiant (formulaire)
@app.route('/ajouter', methods=['GET', 'POST'])
@login_required  # Nécessite une connexion
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
    return render_template('ajouter_eleve.html')

# Route pour ajouter un professeur (formulaire)
@app.route('/ajouter_professeur', methods=['GET', 'POST'])
@login_required  # Nécessite une connexion
def ajouter_professeur_route():
    if request.method == 'POST':
        nom = request.form['nom']
        matiere = request.form['matiere']
        if nom and matiere:
            ajouter_professeur(nom, matiere)
            flash(f"Professeur {nom} ajouté avec succès.")
            return redirect(url_for('index'))
        else:
            flash("Tous les champs sont obligatoires.")
    return render_template('ajouter_professeur.html')

# Route pour calculer la moyenne d'un étudiant
@app.route('/moyenne', methods=['GET', 'POST'])
@login_required  # Nécessite une connexion
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

# Route pour la page de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nom = request.form['nom']
        mot_de_passe = request.form['mot_de_passe']
        if verifier_utilisateur(nom, mot_de_passe):
            user = User(nom, nom, 'etudiant')  # ou 'professeur' selon le rôle
            login_user(user)
            flash("Connexion réussie.")
            return redirect(url_for('index'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.")
    return render_template('login.html')

# Route pour se déconnecter
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Déconnexion réussie.")
    return redirect(url_for('index'))

# Fonction pour vérifier les informations de l'utilisateur
def verifier_utilisateur(nom, mot_de_passe):
    if os.path.exists(FILENAME_UTILISATEURS):
        with open(FILENAME_UTILISATEURS, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                if row[0] == nom and row[1] == mot_de_passe:  # Vérification du mot de passe
                    return True
    return False

# Fonction pour ajouter un utilisateur (pour l'inscription)
def ajouter_utilisateur(nom, mot_de_passe, role):
    with open(FILENAME_UTILISATEURS, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([nom, mot_de_passe, role])

# Route pour s'inscrire
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form['nom']
        mot_de_passe = request.form['mot_de_passe']
        role = request.form['role']  # 'etudiant' ou 'professeur'
        ajouter_utilisateur(nom, mot_de_passe, role)
        flash(f"Utilisateur {nom} créé avec succès.")
        return redirect(url_for('login'))
    return render_template('inscription.html')

# Route pour ajouter une nouvelle matière
@app.route('/ajouter_matiere', methods=['GET', 'POST'])
@login_required  # Facultatif : Peut être activé pour restreindre l'accès aux utilisateurs connectés
def ajouter_matiere():
    if request.method == 'POST':
        matiere = request.form['matiere']
        if matiere:
            try:
                ajouter_matiere_au_csv(matiere)
                flash(f"Matière '{matiere}' ajoutée avec succès.")
                return redirect(url_for('ajouter_matiere'))
            except Exception as e:
                flash("Erreur lors de l'ajout de la matière. Veuillez réessayer.")
        else:
            flash("Le nom de la matière est obligatoire.")
    
    # Lire les matières existantes en dehors du `if`
    matieres = lire_matieres()
    return render_template('ajouter_matiere.html', matieres=matieres)


# Fonction pour ajouter une matière au fichier CSV
def ajouter_matiere_au_csv(matiere):
    FILENAME_MATIERES = 'matieres.csv'
    with open(FILENAME_MATIERES, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([matiere])

# Fonction pour lire toutes les matières
def lire_matieres():
    matieres = []
    if os.path.exists(FILENAME_MATIERES):
        with open(FILENAME_MATIERES, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Sauter l'en-tête
            for row in reader:
                matieres.append(row[0])  # Récupère uniquement le nom de la matière
    return matieres

# Initialisation des fichiers
initialiser_fichiers()

# Démarrage de l'application Flask
if __name__ == '__main__':
    app.run(debug=True)
