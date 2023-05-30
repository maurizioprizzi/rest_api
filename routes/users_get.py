# users_get.py

from flask import Blueprint, jsonify
import sqlite3
from contextlib import closing

# Cria um blueprint para a rota de listagem de usuários
users_get_routes = Blueprint('users_get_routes', __name__)

# Rota para listagem de usuários
@users_get_routes.route('/users', methods=['GET'])
def get_all_users():
    with closing(sqlite3.connect('estoque.db')) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Executa uma consulta para obter todos os usuários do banco de dados
        cursor.execute('SELECT * FROM users')
        rows = cursor.fetchall()

        users = []
        for row in rows:
            user = {
                'id': row['id'],
                'name': row['name'],
                'email': row['email']
            }
            users.append(user)

    return jsonify(users), 200
