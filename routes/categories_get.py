# categories_get.py

from flask import Blueprint, jsonify
import sqlite3

# Cria um blueprint para a rota de listagem de categorias
categories_get_routes = Blueprint('categories_get_routes', __name__)

# Rota para listagem de categorias
@categories_get_routes.route('/categories', methods=['GET'])
def get_categories():
    with sqlite3.connect('estoque.db') as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa uma consulta para obter as categorias do banco de dados
        cursor.execute('SELECT * FROM categories')
        rows = cursor.fetchall()

        categories = []
        for row in rows:
            category = {
                'id': row['id'],
                'name': row['name']
            }
            categories.append(category)

    return jsonify(categories), 200
