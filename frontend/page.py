import requests

from utils import *


def update_user_page(name, description, activity, visible):
    header = getAuthorizationHeader()
    if(header is None):
        return {
            "success": False
        }

    response = requests.post(f"{API_URL}/page",json={
        "description" : description,
        "page_name" : name,
        "visible" : visible,
        "activity" : activity

    }, headers=header)

    return {
        "success" : (response.status_code==200)
    }

def get_user_page():
    header = getAuthorizationHeader()
    if(header is None):
        return {
            "success": False
        }

    response = requests.get(f"{API_URL}/page", headers=header)
    if response.status_code == 200:
        page_data = response.json()
        
        disponibilitesResponse = requests.get(f"{API_URL}/page/disponibilities", headers=header)
        disponibilities = {}
        if disponibilitesResponse.status_code == 200:
            disponibilities["booked"] = [{"date": isoDateToHumanDate(dispo['date']), "id": dispo['id'], "name": dispo["name"], "mail": dispo["mail"]} for dispo in (disponibilitesResponse.json())["booked"]]
            disponibilities["free"] = [{"date": isoDateToHumanDate(dispo['date']), "id": dispo['id']} for dispo in (disponibilitesResponse.json())["free"]]
        return {
            "success" : True,
            "page_data": page_data,
            "disponibilities": disponibilities
        }
    else:
        return {
            "success" : False
        }


def get_page_by_id(pageId):
    response = requests.get(f"{API_URL}/page/{pageId}")
    if response.status_code == 200:
        page_data = response.json()

        disponibilitesResponse = requests.get(f"{API_URL}/page/{pageId}/disponibilities")
        disponibilities = {}
        if disponibilitesResponse.status_code == 200:
            disponibilities["free"] = [{"date": isoDateToHumanDate(dispo['date']), "id": dispo['id'], "page_id": dispo["page_id"]} for dispo in (disponibilitesResponse.json())["free"]]

        return {
            "success" : True,
            "page_data": page_data,
            "disponibilities": disponibilities
        }
    else:
        return {
            "success" : False
        }


def get_recommended_pages():
    response = requests.get(f"{API_URL}/recommended")
    if response.status_code == 200:
        return {
            "success": True,
            "pages": response.json()
        }
    else:
        return {
            "success": False
        }


def search_pages(query):
    result = []
    if(not (query == None or query =="")):

        response = requests.get(f"{API_URL}/search?query={query}")
        if response.status_code == 200:
            results = response.json()
        else:
            return {
                "success": False,
                "message": "Error, search not available."
            }

    return {
        "success": True,
        "results": results
    }