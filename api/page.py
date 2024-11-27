from flask import jsonify
from authentification import authenticate_token
from database import *

def get_page(pageId):
    try:
        page = executeQuery("SELECT * FROM Page WHERE id = ?", (pageId,))

        print(page["visible"])
        if(page["visible"] == '0'):
            return jsonify({'error': 'Page does not exist'}), 404

        page_data = {
            "id": page['id'],
            "page_name": page['page_name'],
            "description": page['description'],
            "activity" : page['activity'],
            "visible": page['visible']
        }

        return jsonify(page_data), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Page does not exist'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


def get_user_page(userId):
    try:
        page = executeQuery("SELECT * FROM Page WHERE user_id = ?", (userId,))

        page_data = {
            "id": page['id'],
            "page_name": page['page_name'],
            "description": page['description'],
            "activity" : page['activity'],
            "visible": page['visible']
        }

        return jsonify(page_data), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'User does not have a page'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

def create_page(userId, pageName, description, activity, visible):

    #Check if all inputs are defined
    if(userId is None or visible is None or pageName is None or description is None or activity is None):
        return jsonify({'error': 'All fields are required.'}), 400
    
    #Call to database
    try:
        executeUpdate("INSERT INTO Page (user_id, visible, page_name, description, activity) VALUES (?, ?, ?, ?, ?)", (userId, visible, pageName, description, activity))
        return jsonify({'message': 'Page created'}), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'User already have a page.'}), 404
    
    except sqlite3.Error as e:
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
        executeUpdate("UPDATE Page SET visible = ?, page_name = ?, description = ?, activity = ? WHERE user_id = ?", (visible, pageName, description, activity, userId))
        return jsonify({'message': 'Page updated'}), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Integrity error'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
