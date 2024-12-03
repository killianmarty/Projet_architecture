import requests
from flask import request, flash

from utils import *

def book_disponibility(pageId, disponibilityId, name, mail):
	response = requests.post(f"{API_URL}/page/{pageId}/disponibilities/{disponibilityId}", json={"name": name, "mail": mail})
	if(response.status_code == 200):
		return {"success": True, "name": name, "mail": mail, "cancel_code": response.json()["cancel_code"]}
	else:
		return {"success": False, "message": "La réservation est déjà prise."}

def free_disponibility(cancelCode):
	if(cancelCode == None or cancelCode ==""):
		return {
			"success": False,
			"message": "No cancel code provided."
		}

	response = requests.delete(f"{API_URL}/cancel", json={"cancel_code": cancelCode})
	if response.status_code == 200:
		results = response.json()
		return {
			"success": True
		}
	else:
		return {
			"success": False,
			"message": "Error, booking does not exist."
		}

def create_disponibility(date):
	header = getAuthorizationHeader()
	if(header is None):
		return {
			"success": False
		}

	requests.post(f"{API_URL}/page/disponibilities", json={"date": request.form["date"]}, headers=header)
	return {
		"success": True
	}

def delete_disponibility(disponibilityId):
	header = getAuthorizationHeader()
	if(header is None):
		return {
			"success": False,
			"allowed": False
		}

	response = requests.delete(f"{API_URL}/page/disponibilities/{disponibilityId}", headers=header)
	if response.status_code == 200:
		return {
			"success" : True
		}
	else:
		return {
			"success": False,
			"allowed": True
		}