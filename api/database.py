import mysql.connector
from mysql.connector import Error
from flask import g

# Configuration de la base de données
import os

DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'mysql'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'password'),
    'database': os.getenv('DB_NAME', 'MkReservation')
}

def get_db():
    if not hasattr(g, 'db'):
        try:
            g.db = mysql.connector.connect(
                host=DATABASE_CONFIG['host'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                database=DATABASE_CONFIG['database']
            )
        except Error as e:
            print(f"Erreur lors de la connexion à la base de données : {e}")
            raise
    return g.db

def executeQuery(query, args=()):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, args)
    result = cursor.fetchone()
    cursor.close()
    return result

def executeQueryAll(query, args=()):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    return result

def executeUpdate(query, args=()):
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query, args)
        db.commit()
    except Error as e:
        db.rollback()
        print(f"Erreur lors de l'exécution de la requête : {e}")
        raise
    finally:
        cursor.close()
