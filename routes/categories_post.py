from flask import Blueprint, jsonify, request
import sqlite3

categories_post_routes = Blueprint('categories_post_routes', __name__)

@categories_post_routes.route('/categories', methods=['POST'])
def create_category():
    conn = None
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()

        data = request.get_json()
        name = data.get('name', None)
        if not name:
            return jsonify({'error': 'Nome de categoria necessário'}), 400

        cursor.execute('SELECT * FROM categories WHERE name = ?', (name,))
        existing_category = cursor.fetchone()
        if existing_category:
            return jsonify({'error': 'Categoria já existente'}), 400

        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()
        category_id = cursor.lastrowid

        return jsonify({'id': category_id, 'name': name}), 201

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Erro desconhecido: {}'.format(str(e))}), 500
    finally:
        if conn:
            conn.close()
