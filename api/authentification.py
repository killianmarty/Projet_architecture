from database import *
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import jsonify, request

SECRET_KEY = 'xFUIOWIarlY5hBQU9lLunttJ7nPlfqGF'

def authenticate_token():
    token = request.headers.get('Authorization')
    print(token)
    if not token:
        return None
    try:
        token = token.split(" ")[1]  # "Bearer <token>"
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token['userId']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None




def signin(username, password, firstName, lastName):
    
    if not username or not password or not firstName or not lastName:
        return jsonify({'error': 'All fields are required.'}), 400

    #Check if user already exists
    user = executeQuery("SELECT * FROM User WHERE username = ?", (username,))

    if user:
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    #Call to database
    executeUpdate("INSERT INTO User (firstName, lastName, username, password) VALUES (?, ?, ?, ?)", (firstName, lastName, username, hashed_password,))

    #Login to new user
    loginResult = login(username, password)
   
    if(loginResult[1] == 200):
        loginResultJSON = loginResult[0].json
        return jsonify({'message': 'User created', 'token': loginResultJSON['token'], 'userId': loginResultJSON['userId']}), 200
    else:
        return jsonify({'message': 'Cannot login to new user'}), 400




def login(username, password):

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    #Check username and password
    user = executeQuery("SELECT * FROM User WHERE username = ?", (username,))

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):

        # Generate JWT Token
        token = jwt.encode({
            'userId': user['id'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify({'token': token, 'userId': user['id']}), 200

    return jsonify({'error': 'Invalid credentials'}), 400