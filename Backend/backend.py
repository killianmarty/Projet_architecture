import datetime
import locale
from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import pytz

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Nécessaire pour les messages flash

# URL de l'API (assurez-vous qu'il correspond à votre serveur API Flask)
API_URL = "http://127.0.0.1:5000"

def getAuthorizationHeader():
    token = session.get('token')
    if(not token):
        return None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return headers

def isoDateToHumanDate(isoDate):
    locale.setlocale(locale.LC_TIME, '')
    date_obj = datetime.datetime.fromisoformat(isoDate)
    date_obj = date_obj.astimezone(pytz.timezone('America/Toronto'))
    return date_obj.strftime("%A %d %B %Y, %H:%M")

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

            token = response.json().get('token')
            session['token'] = token

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

        if response.status_code == 200:
            flash("Inscription réussie !", "success")

            token = response.json().get('token')
            session['token'] = token

            return redirect(url_for("professionnel"))  # Redirige vers la page de connexion après inscription
        else:
            flash("Erreur lors de l'inscription. Veuillez réessayer.", "danger")

    return render_template("inscription.html")

# @app.route("/disponibilites/<int:pageId>", methods=["GET", "POST"])
# def disponibilites(pageId):
#     if request.method == "POST":
#         date = request.form["date"]

#         header = getAuthorizationHeader()
#         if(header is None):
#             return redirect(url_for("connexion"))
        
#         # Appel API pour ajouter une disponibilité
#         response = requests.post(f"{API_URL}/page/{pageId}/disponibilities", json={"date": date}, headers=header)
        
#         if response.status_code == 200:
#             flash("Disponibilité ajoutée.", "success")
#         else:
#             flash("Erreur lors de l'ajout de la disponibilité.", "danger")

#         return redirect(url_for("disponibilites", pageId=pageId))

#     # Récupérer les disponibilités pour la page donnée
#     response = requests.get(f"{API_URL}/page/{pageId}")
    
#     if response.status_code == 200:
#         disponibilites = response.json()
#     else:
#         disponibilites = []

#     return render_template("disponibilites.html", disponibilites=disponibilites)

@app.route("/page", methods=["GET", "POST"])
def professionnel():
    header = getAuthorizationHeader()
    if(header is None):
        return redirect(url_for("connexion"))

    if request.method == "POST":

        page_name = request.form["page_name"]
        description = request.form["description"]
        visible = request.form["visible"] == 'true' 
        activity = request.form["activity"]


        response = requests.post(f"{API_URL}/page",json={
            "description" : description,
            "page_name" : page_name,
            "visible" : visible,
            "activity" : activity

        }, headers=header)

    

    response = requests.get(f"{API_URL}/page", headers=header)
    if response.status_code == 200:
        page_data = response.json()  # Récupère les données au format JSON
        
        disponibilitesResponse = requests.get(f"{API_URL}/page/disponibilities", headers=header)
        disponibilities = {}
        if disponibilitesResponse.status_code == 200:
            disponibilities["booked"] = [{"date": isoDateToHumanDate(dispo['date']), "id": dispo['id']} for dispo in (disponibilitesResponse.json())["booked"]]
            disponibilities["free"] = [{"date": isoDateToHumanDate(dispo['date']), "id": dispo['id']} for dispo in (disponibilitesResponse.json())["free"]]
        return render_template("professionnel.html",  page_name=page_data['page_name'],  description=page_data['description'], visible=page_data['visible'],activity=page_data['activity'], disponibilities=disponibilities)
    else:
                # Si la page n'existe pas ou une erreur se produit, on retourne une page d'erreur ou des données par défaut
        return "404"
       
@app.route("/page/<int:pageId>", methods=["GET"])
def pro(pageId):
   
    response = requests.get(f"{API_URL}/page/{pageId}")
    if response.status_code == 200:
        page_data = response.json()  # Récupère les données au format JSON

        disponibilitesResponse = requests.get(f"{API_URL}/page/{pageId}/disponibilities")
        disponibilities = {}
        if disponibilitesResponse.status_code == 200:
            disponibilities["free"] = [{"date": isoDateToHumanDate(dispo['date']), "id": dispo['id']} for dispo in (disponibilitesResponse.json())["free"]]

        return render_template("professionnel_public.html",  page_name=page_data['page_name'],  description=page_data['description'], visible=page_data['visible'],activity=page_data['activity'], disponibilities=disponibilities)
    else:
                # Si la page n'existe pas ou une erreur se produit, on retourne une page d'erreur ou des données par défaut
        return "404"
    
@app.route("/page/disponibilite", methods=["POST"])
def ajout_disponibilite():
    header = getAuthorizationHeader()
    if(header is None):
        return redirect(url_for("connexion"))

    date = request.form["date"]
    response = requests.post(f"{API_URL}/page/disponibilities", json={"date": date}, headers=header)
    if response.status_code == 200:
        flash("Disponibilité ajoutée.", "success")
    else:
        flash("Erreur lors de l'ajout de la disponibilité.", "danger")
    return redirect(url_for("professionnel"))

@app.route("/page/disponibilite/<int:disponibilityId>", methods=["DELETE"])
def supprimer_disponibilite(disponibilityId):
    header = getAuthorizationHeader()
    if(header is None):
        return redirect(url_for("connexion"))

    response = requests.delete(f"{API_URL}/page/disponibilities/{disponibilityId}", headers=header)
    if response.status_code == 200:
        flash("Disponibilité supprimée.", "success")
    else:
        flash("Erreur lors de la suppression de la disponibilité.", "danger")
    return redirect(url_for("professionnel"))

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("query")
    if(query == None):
        return "No query provided."

    response = requests.get(f"{API_URL}/search?query={query}")
    if response.status_code == 200:
        results = response.json()
        return render_template("recherche.html", results=results)
    else:
        return "Error, search not available."

if __name__ == "__main__":
    app.run(port=5001, debug=True)
