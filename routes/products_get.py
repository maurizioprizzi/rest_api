from flask import Blueprint, jsonify, request
import sqlite3
from utils.pagination import Pagination

# Cria um blueprint para a rota de listagem de produtos
products_get_routes = Blueprint('products_get_routes', __name__)

# Rota para listar todos os produtos com paginação
@products_get_routes.route('/products', methods=['GET'])
def get_all_products():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Obtém a página atual da query string
    page = int(request.args.get('page', 1))
    per_page = 15

    # Obtém todos os produtos do banco de dados
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()

    conn.close()

    # Aplica a paginação aos produtos
    paginator = Pagination(products, page, per_page)
    paginated_products = paginator.paginate()

    # Retorna os produtos paginados
    return jsonify(paginated_products)
