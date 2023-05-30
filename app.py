from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask import Blueprint, jsonify, request

app = Flask(__name__)

# Configuração do JWT
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
app.config['JWT_SETTINGS'] = {
    'JWT_TOKEN_LOCATION': ['headers', 'json']
}
jwt = JWTManager(app)


from routes.auth import auth_routes
from routes.auth_refresh import auth_refresh_routes
from routes.categories_get import categories_get_routes
from routes.categories_post import categories_post_routes
from routes.products_post import products_post_routes
from routes.products_get import products_get_routes
from routes.users_post import users_post_routes
from routes.users_get import users_get_routes
from routes.inventory_post import inventory_add_routes

app.register_blueprint(auth_routes)
app.register_blueprint(auth_refresh_routes)
app.register_blueprint(categories_get_routes)
app.register_blueprint(categories_post_routes)
app.register_blueprint(products_post_routes)
app.register_blueprint(products_get_routes)
app.register_blueprint(users_post_routes)
app.register_blueprint(users_get_routes)
app.register_blueprint(inventory_add_routes)

if __name__ == '__main__':
    app.run(debug=True)
