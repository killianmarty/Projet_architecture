import datetime
import locale
from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import pytz

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Nécessaire pour les messages flash

# URL de l'API (assurez-vous qu'il correspond à votre serveur API Flask)
API_URL = "http://nginx_api:81"

def getAuthorizationHeader():
    token = session.get('token')
    if(not token):
        return None
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return headers

def isoDateToHumanDate(date_obj):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    toronto_tz = pytz.timezone('America/Toronto')
    date_obj = datetime.datetime.strptime(date_obj, "%Y-%m-%d %H:%M:%S")

    date_obj = date_obj.astimezone(toronto_tz)
    return date_obj.strftime("%A %d %b %Y à %H:%M")

@app.route("/")
def home():
    return render_template("accueil.html", logged=(session.get('token') is not None))

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
        return render_template("professionnel.html", logged=(session.get('token') is not None), page_name=page_data['page_name'],  description=page_data['description'], visible=page_data['visible'],activity=page_data['activity'], disponibilities=disponibilities)
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
            disponibilities["free"] = [{"date": isoDateToHumanDate(dispo['date']), "id": dispo['id'], "page_id": dispo["page_id"]} for dispo in (disponibilitesResponse.json())["free"]]

        return render_template("professionnel_public.html", logged=(session.get('token') is not None), page_name=page_data['page_name'],  description=page_data['description'], visible=page_data['visible'],activity=page_data['activity'], disponibilities=disponibilities)
    else:
                # Si la page n'existe pas ou une erreur se produit, on retourne une page d'erreur ou des données par défaut
        return "404"

@app.route("/page/<int:pageId>/disponibilite/<int:disponibilityId>", methods=["POST"])
def page_id_disponibilities_controller_id(pageId, disponibilityId):
   
    data = request.get_json()
    name = data.get('name')
    mail = data.get('mail')

    response = requests.post(f"{API_URL}/page/{pageId}/disponibilities/{disponibilityId}", json={"name": name, "mail": mail})
    if(response.status_code == 200):
        flash("Réservation ajoutée.", "success")
        return {"name": name, "mail": mail, "cancel_code": response.json()["cancel_code"]}
    else:
        flash("Impossible d'ajouter la réservation.", "danger")
        return {"message": "La réservation est déjà prise."}

    

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
    if(query == None or query ==""):
        return render_template("recherche.html", logged=(session.get('token') is not None), results=[])

    response = requests.get(f"{API_URL}/search?query={query}")
    if response.status_code == 200:
        results = response.json()
        return render_template("recherche.html", logged=(session.get('token') is not None), results=results)
    else:
        return "Error, search not available."

@app.route("/cancel", methods=["GET"])
def cancel():
    cancel_code = request.args.get("cancel_code")
    if(cancel_code == None or cancel_code ==""):
        return "No cancel code provided"

    response = requests.delete(f"{API_URL}/cancel", json={"cancel_code": cancel_code})
    if response.status_code == 200:
        results = response.json()
        return render_template("booking_deleted.html", logged=(session.get('token') is not None))
    else:
        return "Error, booking does not exist."

@app.route("/logout")
def logout():
    # Supprimer le token de la session
    session.pop('token', None)

    # Message de confirmation de déconnexion
    flash("Déconnexion réussie.", "success")

    # Rediriger l'utilisateur vers la page d'accueil ou de connexion
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
