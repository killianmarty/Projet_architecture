import random
import string
from authentification import *
from flask import jsonify

def create_disponibility(date):
    userId = authenticate_token()

    if(userId is None):
        return jsonify({'error': 'Unauthorized'}), 401

    if(date is None):
        return jsonify({'error': 'All fields are required.'}), 400
    

    #Verify if logged user is the owner of the page
    result = executeQuery("SELECT id FROM Page WHERE user_id = ?", (userId,))

    if not result:
        return jsonify({'error': 'Page does not exist'}), 404
    
    pageId = result["id"]
    
    #Call to database
    try:
        executeUpdate("INSERT INTO Disponibility (date, page_id) VALUES (?, ?)", (date, pageId,))
        return jsonify({'message': 'Disponibility created'}), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Page does not exist'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    



    
def book_disponibility(pageId, disponibilityId, name, mail):
    if(not (name and mail)):
        return jsonify({'error': 'All fields are required.'}), 400

    #Generate cancel code
    characters = string.ascii_letters + string.digits
    cancelCode = ''.join(random.choice(characters) for _ in range(20))

    #Call to database
    try:
        executeUpdate("INSERT INTO Booking (disponibility_id, cancel_code, mail, name)", (disponibilityId, cancelCode, mail, name))
        return jsonify({'message': 'Booked'}), 200
    
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Disponibility or page does not exist'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    



    
def delete_disponibility(disponibilityId):
    userId = authenticate_token()

    if(userId is None):
        return jsonify({'error': 'Unauthorized'}), 401


    #Verify if logged user is the owner of the page
    result = executeQuery("SELECT id FROM Page WHERE user_id = ?", (userId,))

    if not result:
        return jsonify({'error': 'Page does not exist'}), 404
    
    pageId = result["id"]

    #Call to database
    try:
        executeUpdate("DELETE FROM Disponibility WHERE id = ? AND page_id = ?", (disponibilityId, pageId,))
        return jsonify({'message': 'Disponibility deleted.'}), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Disponibility does not exist'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    
def get_user_disponibilities():
    userId = authenticate_token()

    if(userId is None):
        return jsonify({'error': 'Unauthorized'}), 401


    #Verify if logged user is the owner of the page
    result = executeQuery("SELECT id FROM Page WHERE user_id = ?", (userId,))

    if not result:
        return jsonify({'error': 'Page does not exist'}), 404
    
    return get_disponibilities(result["id"])

def get_disponibilities(pageId):
    try:
        result = executeQueryAll("SELECT * FROM Disponibility WHERE page_id = ?", (pageId,))
        res = [dict(row) for row in result]
        return jsonify(res), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Page does not exist'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500