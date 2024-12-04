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
    result = executeQuery("SELECT id FROM Page WHERE user_id = %s", (userId,))

    if not result:
        return jsonify({'error': 'Page does not exist'}), 404
    
    pageId = result["id"]
    
    #Call to database
    try:
        executeUpdate("INSERT INTO Disponibility (date, page_id) VALUES (%s, %s)", (date, pageId,))
        return jsonify({'message': 'Disponibility created'}), 200

    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Page does not exist'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    



    
def book_disponibility(disponibilityId, name, mail):
    if(not (name and mail)):
        return jsonify({'error': 'All fields are required.'}), 400

    #Generate cancel code
    characters = string.ascii_letters + string.digits
    cancelCode = ''.join(random.choice(characters) for _ in range(20))

    #Call to database
    try:
        #check if disponibility is free
        results = executeQueryAll("SELECT * FROM Booking WHERE disponibility_id = %s;", (disponibilityId,))
        if(len(results) == 0):
            executeUpdate("INSERT INTO Booking (disponibility_id, cancel_code, mail, name) VALUES (%s, %s, %s, %s)", (disponibilityId, cancelCode, mail, name))
            return jsonify({'message': 'Booked', 'cancel_code': cancelCode}), 200
        else:
            return jsonify({'error': 'Disponibility already booked.'}), 400
    
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Disponibility or page does not exist'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    

def free_disponibility(cancel_code):
    if(cancel_code is None):
        return jsonify({'error': 'No cancel code provided.'}), 400

    try:
        executeUpdate("DELETE FROM Booking WHERE cancel_code = %s;", (cancel_code,))
    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Booking does not exist'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
        
    return jsonify({'message': "Booking cancelled."}), 200
    
def delete_disponibility(disponibilityId):
    userId = authenticate_token()

    if(userId is None):
        return jsonify({'error': 'Unauthorized'}), 401


    #Verify if logged user is the owner of the page
    result = executeQuery("SELECT id FROM Page WHERE user_id = %s", (userId,))

    if not result:
        return jsonify({'error': 'Page does not exist'}), 404
    
    pageId = result["id"]

    #Call to database
    try:
        executeUpdate("DELETE FROM Disponibility WHERE id = %s AND page_id = %s", (disponibilityId, pageId,))
        return jsonify({'message': 'Disponibility deleted.'}), 200

    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Disponibility does not exist'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500
    
def get_user_disponibilities():
    userId = authenticate_token()

    if(userId is None):
        return jsonify({'error': 'Unauthorized'}), 401


    #Verify if logged user is the owner of the page
    result = executeQuery("SELECT id FROM Page WHERE user_id = %s", (userId,))

    if not result:
        return jsonify({'error': 'Page does not exist'}), 404
    
    return get_disponibilities(result["id"])

def get_disponibilities(pageId):
    try:
        unbooked = executeQueryAll("SELECT date, id, page_id FROM Disponibility LEFT JOIN Booking ON Disponibility.id = Booking.disponibility_id WHERE page_id = %s AND disponibility_id IS NULL", (pageId,))
        res1 = [dict(row) for row in unbooked]
        for row in res1:
            row["date"] = row["date"].strftime("%Y-%m-%d %H:%M:%S")
        
        booked = executeQueryAll("SELECT date, id, page_id, mail, name FROM Disponibility JOIN Booking ON Disponibility.id = Booking.disponibility_id WHERE page_id = %s", (pageId,))
        res2 = [dict(row) for row in booked]
        for row in res2:
            row["date"] = row["date"].strftime("%Y-%m-%d %H:%M:%S")

        return jsonify({"booked": res2, "free": res1}), 200

    except mysql.connector.IntegrityError:
        return jsonify({'error': 'Page does not exist'}), 404
    
    except mysql.connector.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500