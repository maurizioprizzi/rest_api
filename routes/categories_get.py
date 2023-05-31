from flask import Blueprint, jsonify, current_app
import sqlite3
from sqlite3 import Error
import logging

categories_get_routes = Blueprint('categories_get_routes', __name__)

def get_db_connection():
    try:
        conn = sqlite3.connect('estoque.db')
        conn.row_factory = sqlite3.Row
        return conn, None
    except Error as e:
        logging.error(str(e))
        return None, "Cannot establish a DB connection"

def get_categories_db():
    conn, error = get_db_connection()
    if conn is None:
        return None, error, 500
    
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM categories')
        rows = cursor.fetchall()

        categories = []
        for row in rows:
            categories.append({'id': row['id'], 'name': row['name']})

        return categories, None, 200
    except Error as e:
        logging.error(str(e))
        return None, str(e), 500
    finally:
        conn.close()

@categories_get_routes.route('/categories', methods=['GET'])
def get_categories():
    categories, error, status_code = get_categories_db()
    if categories is None:
        return jsonify({'error': error}), status_code
    else:
        return jsonify(categories), status_code
