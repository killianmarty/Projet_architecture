import sqlite3
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, g
import random
import string


app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète_pour_jwt'

DATABASE = '../database/database.db'


def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    with app.app_context():
        db = get_db()
        

def authenticate_token():
    token = request.headers.get('Authorization')
    if not token:
        return None
    try:
        token = token.split(" ")[1]  # "Bearer <token>"
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded_token['userId']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    firstName = data.get('firstName')
    lastName = data.get('lastName')

    if not username or not password or not firstName or not lastName:
        return jsonify({'error': 'All fields are required.'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO User (firstName, lastName, username, password) VALUES (?, ?, ?, ?)", (firstName, lastName, username, hashed_password))
    db.commit()

    return jsonify({'message': 'User created'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        # Générer le token JWT
        token = jwt.encode({
            'username': user['username'],
            'userId': user['id'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'}), 400


@app.route('/page', methods=['POST'])
def create_page():
    userId = authenticate_token()
    if not userId:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    visible = data.get('visible')
    pageName = data.get('page_name')
    description = data.get('description')

    if(not (visible and pageName and description)):
        return jsonify({'error': 'All fields are required.'}), 400

    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("INSERT INTO Page (user_id, visible, page_name, description) VALUES (?, ?, ?, ?)", (userId, visible, pageName, description))
        db.commit()
        return jsonify({'message': 'Page created'}), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'User already have a page.'}), 404
    except sqlite3.Error as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500


@app.route('/page/<int:pageId>', methods=['GET'])
def get_page(pageId):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM Page WHERE id = ?", (pageId,))
        page = cursor.fetchone()

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

@app.route('/page/<int:pageId>/disponibilities', methods=['POST'])
def add_disponibility(pageId):
    userId = authenticate_token()

    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT user_id FROM Page WHERE id = ?", (pageId,))
        result = cursor.fetchone()

        if not userId or not (result["user_id"] == userId):
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        date = data.get('date')
        

        if(not (pageId and date)):
            return jsonify({'error': 'All fields are required.'}), 400

        cursor.execute("INSERT INTO Disponibility (date, page_id) VALUES (?, ?)", (date, pageId))
        db.commit()

        return jsonify({'message': 'Disponibility created'}), 201

    except sqlite3.IntegrityError:
        return jsonify({'error': 'Page does not exist'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500

@app.route('/page/<int:pageId>/disponibilities/<int:disponibilityId>', methods=['POST', "DELETE"])
def post_disponibility(pageId, disponibilityId):

    if(request.method == 'POST'):

        data = request.get_json()
        name = data.get('name')
        mail = data.get('mail')

        if(not (name and mail)):
            return jsonify({'error': 'All fields are required.'}), 400

        characters = string.ascii_letters + string.digits
        cancel_code = ''.join(random.choice(characters) for _ in range(20))

        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO Booking (disponibility_id, cancel_code, mail, name)", (disponibilityId, cancelCode, mail, name))
            db.commit()

            return jsonify({'message': 'Booked'}), 201
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Disponibility or page does not exist'}), 404
        except sqlite3.Error as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500


    elif(request.method == 'DELETE'):

        userId = authenticate_token()

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT user_id FROM Page WHERE id = ?", (pageId,))
        result = cursor.fetchone()

        if not userId or not (result["user_id"] == userId):
            return jsonify({'error': 'Unauthorized'}), 401

        try:
            cursor.execute("DELETE FROM Disponibility WHERE id = ? AND page_id = ?", (disponibilityId, pageId))
            db.commit()

            return jsonify({'message': 'Disponibility deleted.'}), 201

        except sqlite3.IntegrityError:
            return jsonify({'error': 'Disponibility or page does not exist'}), 404
        except sqlite3.Error as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500

init_db()

if __name__ == '__main__':
    app.run(debug=True)
