from flask import Blueprint, jsonify, request
import sqlite3
from utils.enc_dec_password import encrypt_password

# Cria um blueprint para a rota de registro de usuários
users_post_routes = Blueprint('users_post_routes', __name__)

# Rota para registro de usuários
@users_post_routes.route('/users', methods=['POST'])
def register_user():
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

    # Verifica se o email já está registrado
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return jsonify({'error': 'O email fornecido já está registrado'}), 400

    # Faz o hash da senha antes de armazená-la no banco de dados
    hashed_password = encrypt_password(password)

    # Insere o usuário no banco de dados
    cursor.execute('INSERT INTO users (email, senha) VALUES (?, ?)', (email, hashed_password))
    conn.commit()

    # Obtém o ID do usuário recém-registrado
    user_id = cursor.lastrowid

    conn.close()

    # Retorna a resposta com o ID do novo usuário
    response = {
        'id': user_id,
        'email': email
    }
    return jsonify(response), 201
