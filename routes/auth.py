from flask import Blueprint, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

# Cria um blueprint para as rotas de autenticação
auth_routes = Blueprint('auth_routes', __name__)

# Configuração do JWT
jwt = JWTManager()

# Rota para autenticação
@auth_routes.route('/auth', methods=['POST'])
def auth():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Verifica se as credenciais são válidas
    if email != 'admin@user.com' or password != '123456':
        return jsonify({"error": "Credenciais inválidas"}), 401

    # Gera um token JWT válido por 5 minutos
    access_token = create_access_token(identity=email, expires_delta=False, fresh=True)
    return jsonify({"access_token": access_token}), 200

# Rota protegida por autenticação
@auth_routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "Rota protegida"})
