from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, JWTManager
from werkzeug.exceptions import BadRequest
from datetime import timedelta

# Cria um blueprint para as rotas de autenticação
auth_routes = Blueprint('auth_routes', __name__)

# Configuração do JWT
jwt = JWTManager()

@jwt.token_in_blocklist_loader
def check_if_token_revoked(decrypted_token):
    jti = decrypted_token['jti']
    return jti in revoked_tokens

@jwt.revoked_token_loader
def handle_token_revoked():
    return jsonify({"error": "Token inválido"}), 401

# Rota para autenticação
@auth_routes.route('/auth', methods=['POST'])
def authenticate():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Validação dos campos de entrada
    if not email or not password:
        raise BadRequest("E-mail e senha são campos obrigatórios")

    # Verifica se as credenciais são válidas
    if email != 'admin@user.com' or password != '123456':
        return jsonify({"error": "Credenciais inválidas"}), 401

    # Gera um token JWT válido por 5 minutos
    access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=5), fresh=True)
    return jsonify({"access_token": access_token}), 200

# Rota protegida por autenticação
@auth_routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({"message": "Rota protegida"})

# Lista de tokens revogados
revoked_tokens = set()

def revoke_token(jti):
    revoked_tokens.add(jti)

def unrevoke_token(jti):
    revoked_tokens.remove(jti)

