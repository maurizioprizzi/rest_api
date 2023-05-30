from flask import Flask

app = Flask(__name__)

# Importa as rotas de autenticação do arquivo routes/auth.py
from routes.auth import auth_routes
# Importa as rotas de renovação do token de acesso do arquivo routes/auth_refresh.py
from routes.auth_refresh import auth_refresh_routes
# Importa a rota de listagem de categorias do arquivo routes/categories_get.py
from routes.categories_get import categories_get_routes
# Importa a rota de inserção de categorias do arquivo routes/categories_post.py
from routes.categories_post import categories_post_routes
# Importa a rota de inserção de produtos do arquivo routes/products_post.py
from routes.products_post import products_post_routes

# Registra as rotas de autenticação no aplicativo Flask
app.register_blueprint(auth_routes)
# Registra as rotas de renovação do token de acesso no aplicativo Flask
app.register_blueprint(auth_refresh_routes)
# Registra a rota de listagem de categorias no aplicativo Flask
app.register_blueprint(categories_get_routes)
# Registra a rota de inserção de categorias no aplicativo Flask
app.register_blueprint(categories_post_routes)
# Registra a rota de inserção de produtos no aplicativo Flask
app.register_blueprint(products_post_routes)

# Configuração do JWT
from flask_jwt_extended import JWTManager

app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Defina uma chave secreta para assinar os tokens JWT
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run(debug=True)
