from flask import Flask

app = Flask(__name__)

# Importa as rotas de autenticação do arquivo routes/auth.py
from routes.auth import auth_routes
# Importa as rotas de renovação do token de acesso do arquivo routes/auth_refresh.py
from routes.auth_refresh import auth_refresh_routes

# Registra as rotas de autenticação no aplicativo Flask
app.register_blueprint(auth_routes)
# Registra as rotas de renovação do token de acesso no aplicativo Flask
app.register_blueprint(auth_refresh_routes)

# Configuração do JWT
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Defina uma chave secreta para assinar os tokens JWT
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
