from flask import jsonify
from authentification import authenticate_token
from database import *

def get_page(pageId):
    try:
        page = executeQuery("SELECT * FROM Page WHERE id = ?", (pageId,))

        page_data = {
            "id": page['id'],
            "page_name": page['page_name'],
            "description": page['description'],
            "visible": page['visible']
        }

        return jsonify(page_data), 201

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Page does not exist'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

def create_page(pageName, description, visible):
    userId = authenticate_token()

    if not userId:
        return jsonify({'error': 'Unauthorized'}), 401

    if(not visible or not pageName or not description):
        return jsonify({'error': 'All fields are required.'}), 400

    
    #Call to database
    try:
        executeUpdate("INSERT INTO Page (user_id, visible, page_name, description) VALUES (?, ?, ?, ?)", (userId, visible, pageName, description))
        return jsonify({'message': 'Page created'}), 201

    except sqlite3.IntegrityError:
        return jsonify({'error': 'User already have a page.'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500