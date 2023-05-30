from flask import Flask

app = Flask(__name__)

from routes.auth import auth_routes
from routes.auth_refresh import auth_refresh_routes
from routes.categories_get import categories_get_routes
from routes.categories_post import categories_post_routes
from routes.products_post import products_post_routes
from routes.products_get import products_get_routes
from routes.users_post import users_post_routes
from routes.users_get import users_get_routes

app.register_blueprint(auth_routes)
app.register_blueprint(auth_refresh_routes)
app.register_blueprint(categories_get_routes)
app.register_blueprint(categories_post_routes)
app.register_blueprint(products_post_routes)
app.register_blueprint(products_get_routes)
app.register_blueprint(users_post_routes)
app.register_blueprint(users_get_routes)

# Configuração do JWT
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Defina uma chave secreta para assinar os tokens JWT
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
