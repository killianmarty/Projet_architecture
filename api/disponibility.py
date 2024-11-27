import random
import string
from authentification import *
from flask import jsonify

def create_disponibility(pageId, date):
    userId = authenticate_token()

    if(not (pageId and date)):
        return jsonify({'error': 'All fields are required.'}), 400
    

    #Verify if logged user is the owner of the page
    result = executeQuery("SELECT user_id FROM Page WHERE id = ?", (pageId,))

    if not result:
        return jsonify({'error': 'Page does not exist'}), 404
    
    if not userId or not (result["user_id"] == userId):
        return jsonify({'error': 'Unauthorized'}), 401

    
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
    



    
def delete_disponibility(pageId, disponibilityId):
    userId = authenticate_token()

    #Verify if logged user is the owner of the page
    result = executeQuery("SELECT user_id FROM Page WHERE id = ?", (pageId,))

    if not result:
        return jsonify({'error': 'Page does not exist'}), 404

    if not userId or not (result["user_id"] == userId):
        return jsonify({'error': 'Unauthorized'}), 401

    #Call to database
    try:
        executeUpdate("DELETE FROM Disponibility WHERE id = ? AND page_id = ?", (disponibilityId, pageId,))
        return jsonify({'message': 'Disponibility deleted.'}), 200

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Disponibility does not exist'}), 404
    
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500