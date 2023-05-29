from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

# Cria um blueprint para as rotas de renovação do token de acesso
auth_refresh_routes = Blueprint('auth_refresh_routes', __name__)

# Rota para renovar o token de acesso
@auth_refresh_routes.route('/auth/refresh', methods=['POST'])
@jwt_required()
def refresh():
    # Obtém a identidade do token JWT atual
    current_identity = get_jwt_identity()

    # Gera um novo token de acesso válido por 5 minutos
    new_access_token = create_access_token(identity=current_identity, expires_delta=False, fresh=False)

    return jsonify({"access_token": new_access_token}), 200
