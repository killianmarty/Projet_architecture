import requests
from flask import flash, session

from utils import *

def login(username, password):
    response = requests.post(f"{API_URL}/login", json={
        "username": username,
        "password": password
    })
    
    if response.status_code == 200:
        flash("Connexion réussie.", "success")

        token = response.json().get('token')
        return {
            "success" : True,
            "token": token 
        }
    else:
        flash("Identifiants incorrects.", "danger")
        return {
            "success" : False
        }

def logout():
    session.pop('token', None)
    flash("Déconnexion réussie.", "success")

def signin(firstName, lastName, username, password):
    response = requests.post(f"{API_URL}/signin", json={
        "first_name": firstName,
        "last_name": lastName,
        "username": username,
        "password": password
    })

    if response.status_code == 200:
        flash("Inscription réussie !", "success")

        token = response.json().get('token')
        return {
            "success" : True,
            "token": token 
        }
    else:
        flash("Erreur lors de l'inscription. Veuillez réessayer.", "danger")
        return {
            "success" : False
        }