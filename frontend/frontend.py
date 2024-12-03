from flask import Flask, render_template, request, redirect, url_for, session

from authentification import *
from page import *
from disponibility import *
from utils import *

app = Flask(__name__)
app.secret_key = "38v55ZveT6Pout1r7KZR"


@app.route("/")
def home_controller():
    get_recommended_pages_result = get_recommended_pages()
    if(get_recommended_pages_result["success"]):
        return render_template("accueil.html", logged=(session.get('token') is not None), recommended_pages=get_recommended_pages_result["pages"])
    else:
        return render_template("accueil.html", logged=(session.get('token') is not None))


@app.route("/connexion", methods=["GET", "POST"])
def login_controller():
    if request.method == "POST":
        login_result = login(request.form["nom-utilisateur"], request.form["motdepasse"])
        if(login_result["success"]):
            session['token'] = login_result["token"]
            return redirect(url_for("page_controller"))
        else:
            return render_template("connexion.html", error=login_result["message"])

    return render_template("connexion.html")



@app.route("/logout")
def logout_controller():
    logout()
    return redirect(url_for("home_controller"))



@app.route("/inscription", methods=["GET", "POST"])
def signin_controller():
    if request.method == "POST":
        signin_result = signin(request.form["prenom"], request.form["nom"], request.form["nom-utilisateur"], request.form["motdepasse"])
        if(signin_result["success"]):
            session['token'] = signin_result["token"]
            return redirect(url_for("page_controller"))
        else:
            return render_template("inscription.html", error=signin_result["message"])

    return render_template("inscription.html")



@app.route("/page", methods=["GET", "POST"])
def page_controller():
    header = getAuthorizationHeader()
    if(header is None):
        return redirect(url_for("login_controller"))

    if request.method == "POST":

        create_user_page_result = update_user_page(request.form["page_name"], request.form["description"], request.form["activity"], request.form["visible"] == 'true')
        if(create_user_page_result["success"] == False):
            return redirect(url_for("login_controller"))
    
    get_user_page_result = get_user_page()
    if(get_user_page_result["success"]):
        return render_template("professionnel.html", logged=(session.get('token') is not None), page_name=get_user_page_result["page_data"]['page_name'],  description=get_user_page_result["page_data"]['description'], visible=get_user_page_result["page_data"]['visible'],activity=get_user_page_result["page_data"]['activity'], disponibilities=get_user_page_result["disponibilities"])
    else:
        return render_template("error.html", error_code=404)
      


@app.route("/page/disponibilite", methods=["POST"])
def page_disponibility_controller():
    create_disponibility_result = create_disponibility(request.form["date"])
    if(create_disponibility_result["success"]):
        return redirect(url_for("page_controller"))
    else:
        return redirect(url_for("login_controller"))



@app.route("/page/disponibilite/<int:disponibilityId>", methods=["DELETE"])
def page_disponibility_id_controller(disponibilityId):
    delete_disponibility_result = delete_disponibility(disponibilityId)
    if(delete_disponibility_result["success"]):
        return redirect(url_for("page_controller"))
    elif(delete_disponibility_result["allowed"]):
        return redirect(url_for("page_controller"))
    else:
        return redirect(url_for("login_controller"))




@app.route("/page/<int:pageId>", methods=["GET"])
def page_id_controller(pageId):
    get_page_by_id_result = get_page_by_id(pageId)
    if(get_page_by_id_result["success"]):
        return render_template("professionnel_public.html", logged=(session.get('token') is not None), page_name=get_page_by_id_result["page_data"]['page_name'],  description=get_page_by_id_result["page_data"]['description'], visible=get_page_by_id_result["page_data"]['visible'],activity=get_page_by_id_result["page_data"]['activity'], disponibilities=get_page_by_id_result["disponibilities"])
    else:
        return render_template("error.html", error_code=404)


@app.route("/page/<int:pageId>/disponibilite/<int:disponibilityId>", methods=["POST"])
def page_id_disponibilities_controller_id(pageId, disponibilityId):
    data = request.get_json()
    return book_disponibility(pageId, disponibilityId, data.get('name'), data.get('mail'))

    

@app.route("/search", methods=["GET"])
def search_controller():
    search_pages_result = search_pages(request.args.get("query"))
    if(search_pages_result["success"]):
        return render_template("recherche.html", logged=(session.get('token') is not None), results=search_pages_result["results"])
    else:
        return render_template("recherche.html", error=search_pages_result["message"])

@app.route("/cancel", methods=["GET"])
def cancel_controller():
    free_disponibility_result = free_disponibility(request.args.get("cancel_code"))
    if(free_disponibility_result["success"]):
        return render_template("booking_deleted.html", logged=(session.get('token') is not None))
    else:
        return free_disponibility_result["message"]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
