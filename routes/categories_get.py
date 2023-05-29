from flask import Blueprint, jsonify
import sqlite3

# Cria um blueprint para a rota de listagem de categorias
categories_get_routes = Blueprint('categories_get_routes', __name__)

# Rota para listagem de categorias
@categories_get_routes.route('/categories', methods=['GET'])
def get_categories():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Executa uma consulta para obter as categorias do banco de dados
    cursor.execute('SELECT * FROM categories')
    rows = cursor.fetchall()

    categories = []
    for row in rows:
        category = {
            'id': row[0],
            'name': row[1]
        }
        categories.append(category)

    conn.close()

    return jsonify(categories), 200
