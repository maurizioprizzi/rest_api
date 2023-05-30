from flask import Blueprint, jsonify, request
import sqlite3
from utils.enc_dec_password import decrypt_password

# Cria um blueprint para a rota de autenticação de usuários
users_get_routes = Blueprint('users_get_routes', __name__)

# Rota para autenticação de usuários
@users_get_routes.route('/users/authenticate', methods=['POST'])
def authenticate_user():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Obtém os dados do usuário do corpo da solicitação
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Verifica se o email e a senha foram fornecidos
    if not email or not password:
        conn.close()
        return jsonify({'error': 'O email e a senha são obrigatórios'}), 400

    # Verifica se o usuário existe no banco de dados
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    existing_user = cursor.fetchone()

    if not existing_user:
        conn.close()
        return jsonify({'error': 'Credenciais inválidas'}), 401

    # Descriptografa a senha e verifica se corresponde à senha fornecida
    if not decrypt_password(existing_user[2], password):
        conn.close()
        return jsonify({'error': 'Credenciais inválidas'}), 401

    conn.close()

    # Retorna a resposta com o ID do usuário autenticado
    response = {
        'id': existing_user[0],
        'email': existing_user[1]
    }
    return jsonify(response), 200

# Rota para listar todos os usuários
@users_get_routes.route('/users', methods=['GET'])
def get_all_users():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Obtém todos os usuários do banco de dados
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    conn.close()

    # Converte cada tupla em um dicionário
    users_list = []
    for user in users:
        user_dict = {
            'id': user[0],
            'email': user[1],
            'password': user[2].decode('utf-8')  # Converte bytes em string
        }
        users_list.append(user_dict)

    # Retorna a lista de usuários
    return jsonify(users_list)

