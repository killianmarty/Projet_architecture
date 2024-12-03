import requests
from flask import flash, session

from utils import *

def login(username, password):
    response = requests.post(f"{API_URL}/login", json={
        "username": username,
        "password": password
    })
    
    if response.status_code == 200:
        token = response.json().get('token')
        return {
            "success" : True,
            "token": token 
        }
    else:
        return {
            "success" : False,
            "message": "Identifiants incorrects."
        }

def logout():
    session.pop('token', None)

def signin(firstName, lastName, username, password):
    response = requests.post(f"{API_URL}/signin", json={
        "first_name": firstName,
        "last_name": lastName,
        "username": username,
        "password": password
    })

    if response.status_code == 200:
        token = response.json().get('token')
        return {
            "success" : True,
            "token": token 
        }
    else:
        return {
            "success" : False,
            "message": "Erreur lors de l'inscription. Veuillez réessayer."
        }