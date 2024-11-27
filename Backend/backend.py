from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Nécessaire pour les messages flash

# URL de l'API (assurez-vous qu'il correspond à votre serveur API Flask)
API_URL = "http://127.0.0.1:5000"

@app.route("/")
def home():
    return render_template("accueil.html")

@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method == "POST":
        username = request.form["nom-utilisateur"]
        password = request.form["motdepasse"]

        # Appel à l'API pour vérifier la connexion
        response = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
        
        if response.status_code == 200:
            flash("Connexion réussie.", "success")
            return redirect(url_for("professionnel"))  # Remplacez par la route réelle du dashboard
        else:
            flash("Identifiants incorrects.", "danger")

    return render_template("connexion.html")

@app.route("/inscription", methods=["GET", "POST"])
def inscription():
    if request.method == "POST":
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        username = request.form["nom-utilisateur"]
        password = request.form["motdepasse"]

        # Appel à l'API pour l'inscription
        response = requests.post(f"{API_URL}/signin", json={
            "first_name": prenom,
            "last_name": nom,
            "username": username,
            "password": password
        })

        if response.status_code == 201:
            flash("Inscription réussie !", "success")
            return redirect(url_for("connexion"))  # Redirige vers la page de connexion après inscription
        else:
            flash("Erreur lors de l'inscription. Veuillez réessayer.", "danger")

    return render_template("inscription.html")

@app.route("/disponibilites/<int:pageId>", methods=["GET", "POST"])
def disponibilites(pageId):
    if request.method == "POST":
        date = request.form["date"]
        
        # Appel API pour ajouter une disponibilité
        response = requests.post(f"{API_URL}/page/{pageId}/disponibilities", json={"date": date})
        
        if response.status_code == 201:
            flash("Disponibilité ajoutée.", "success")
        else:
            flash("Erreur lors de l'ajout de la disponibilité.", "danger")

        return redirect(url_for("disponibilites", pageId=pageId))

    # Récupérer les disponibilités pour la page donnée
    response = requests.get(f"{API_URL}/page/{pageId}")
    
    if response.status_code == 200:
        disponibilites = response.json()
    else:
        disponibilites = []

    return render_template("disponibilites.html", disponibilites=disponibilites)

@app.route("/page")
def professionnel():
    # Récupérer le prénom de l'utilisateur depuis la session
    prenom = session.get('prenom', 'Utilisateur')  # Si pas de prénom, afficher 'Utilisateur'
    return render_template("professionnel.html", prenom=prenom)  # Passer le prénom au template


if __name__ == "__main__":
    app.run(port=5001, debug=True)
