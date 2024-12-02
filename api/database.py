import mysql.connector
from mysql.connector import Error
from flask import g

# Configuration de la base de données
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Remplace par ton utilisateur MySQL
    'password': 'password',  # Remplace par ton mot de passe MySQL
    'database': 'MkReservation'  # Remplace par le nom de ta base de données
}

def get_db():
    """
    Initialise une connexion à la base de données MySQL et la stocke dans le contexte global de Flask (g).
    """
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
    """
    Exécute une requête SELECT qui retourne une seule ligne.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)  # Utilisation de dictionary=True pour obtenir un résultat sous forme de dict
    cursor.execute(query, args)
    result = cursor.fetchone()
    cursor.close()
    return result

def executeQueryAll(query, args=()):
    """
    Exécute une requête SELECT qui retourne toutes les lignes.
    """
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    return result

def executeUpdate(query, args=()):
    """
    Exécute une requête d'insertion, de mise à jour ou de suppression.
    """
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
