from flask import Blueprint, jsonify, request
import sqlite3
from utils.enc_dec_password import decrypt_password
from utils.pagination import Pagination

# Cria um blueprint para a rota de autenticação de usuários
users_get_routes = Blueprint('users_get_routes', __name__)

# Rota para listar todos os usuários
@users_get_routes.route('/users', methods=['GET'])
def get_all_users():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Obtém a página atual da query string
    page = int(request.args.get('page', 1))
    per_page = 15

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

    # Aplica a paginação aos usuários
    paginator = Pagination(users_list, page, per_page)
    paginated_users = paginator.paginate()

    # Retorna os usuários paginados
    return jsonify(paginated_users)
