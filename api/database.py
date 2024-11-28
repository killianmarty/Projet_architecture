import sqlite3
from flask import g

DATABASE = '../database/database.db'

def get_db():
    if not hasattr(g, 'db'):
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

def executeQuery(query, args=()):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    result = cursor.fetchone()

    return result

def executeQueryAll(query, args=()):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()

    return result

def executeUpdate(query, args=()):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, args)
    db.commit()

    return