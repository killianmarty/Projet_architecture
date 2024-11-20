import sqlite3
import bcrypt
import jwt
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, g

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_clé_secrète_pour_jwt'

# Base de données SQLite
DATABASE = 'users.db'


# Fonction pour se connecter à la base de données
def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


# Créer la table 'users' si elle n'existe pas déjà
def init_db():
    with app.app_context():
        db = get_db()
        db.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')
        db.commit()


# Fonction pour vérifier le token JWT
def authenticate_token():
    token = request.headers.get('Authorization')
    if not token:
        return None
    try:
        token = token.split(" ")[1]  # "Bearer <token>"
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded_token['username']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


# Route "coucou" accessible à tout le monde
@app.route('/coucou', methods=['GET'])
def coucou():
    return "Coucou tout le monde !"


# Route "signin" pour l'inscription d'un nouvel utilisateur
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        return jsonify({'error': 'User already exists'}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    db.commit()

    return jsonify({'message': 'User created'}), 201


# Route "login" pour la connexion d'un utilisateur
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        # Générer le token JWT
        token = jwt.encode({
            'username': user['username'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'}), 400


# Route "logout" pour la déconnexion (simulée côté client)
@app.route('/logout', methods=['POST'])
def logout():
    # Pour la déconnexion, il suffit de supprimer le token côté client, aucune action serveur n'est nécessaire
    return jsonify({'message': 'Logged out successfully'})


# Route protégée accessible seulement aux utilisateurs connectés
@app.route('/protected', methods=['GET'])
def protected():
    username = authenticate_token()
    if not username:
        return jsonify({'error': 'Unauthorized'}), 401

    return jsonify({'message': f'Hello {username}, you are authenticated and authorized.'})


# Initialiser la base de données (si ce n'est pas déjà fait)
init_db()

# Lancer le serveur Flask
if __name__ == '__main__':
    app.run(debug=True)
