from flask import jsonify
import mysql
from authentification import authenticate_token
from database import *

def get_page(pageId):
    try:
        page = executeQuery("SELECT * FROM Page WHERE id = %s", (pageId,))

        if(page["visible"] == 'false'):
            return jsonify({'error': 'Page does not exist'}), 404

        page_data = {
            "id": page['id'],
            "page_name": page['page_name'],
            "description": page['description'],
            "activity" : page['activity'],
            "visible": page['visible']
        }

        return jsonify(page_data), 200

    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Page does not exist'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


def get_user_page(userId):
    try:
        page = executeQuery("SELECT * FROM Page WHERE user_id = %s", (userId,))

        page_data = {
            "id": page['id'],
            "page_name": page['page_name'],
            "description": page['description'],
            "activity" : page['activity'],
            "visible": page['visible']
        }

        return jsonify(page_data), 200

    except mysql.connector.IntegrityError:
        return jsonify({'error': 'User does not have a page'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


def get_recommended_pages():
    try:
        results = executeQueryAll("SELECT * FROM Page ORDER BY id LIMIT 3", ())
        searchResult = [{"id": result["id"], "page_name": result["page_name"], "description": result["description"], "activity": result["activity"]} for result in results]

        return jsonify(searchResult), 200

    except mysql.connector.IntegrityError:
        return jsonify({'error': 'No pages'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


def create_page(userId, pageName, description, activity, visible):

    #Check if all inputs are defined
    if(userId is None or visible is None or pageName is None or description is None or activity is None):
        return jsonify({'error': 'All fields are required.'}), 400
    
    #Call to database
    try:
        executeUpdate("INSERT INTO Page (user_id, visible, page_name, description, activity) VALUES (%s, %s, %s, %s, %s)", (userId, visible, pageName, description, activity))
        return jsonify({'message': 'Page created'}), 200

    except mysql.connector.IntegrityError:
        return jsonify({'error': 'User already have a page.'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

def update_page(pageName, description, activity, visible):
    userId = authenticate_token()
    
    #Verify if user is logged
    if not userId:
        return jsonify({'error': 'Unauthorized'}), 401

    #Check if all inputs are defined
    if(visible is None or pageName is None or description is None or activity is None):
        return jsonify({'error': 'All fields are required.'}), 400
    
    #Call to database
    try:
        executeUpdate("UPDATE Page SET visible = %s, page_name = %s, description = %s, activity = %s WHERE user_id = %s;", (visible, pageName, description, activity, userId))
        return jsonify({'message': 'Page updated'}), 200

    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Integrity error'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


def search_pages(query):
    if(query == None):
        return jsonify({'error': 'No query provided.'}), 404

    results = executeQueryAll(
        "SELECT * FROM Page WHERE page_name LIKE CONCAT('%', %s, '%') OR description LIKE CONCAT('%', %s, '%') OR activity LIKE CONCAT('%', %s, '%') COLLATE utf8mb4_general_ci;", 
        (query, query, query)
    )
    searchResult = [{"id": result["id"], "page_name": result["page_name"], "description": result["description"], "activity": result["activity"]} for result in results if result["visible"] == "true"]
    
    return jsonify(searchResult), 200
