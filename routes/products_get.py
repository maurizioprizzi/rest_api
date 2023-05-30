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

# Rota para mostrar um produto específico
@products_get_routes.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Obtém o produto do banco de dados pelo ID
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = cursor.fetchone()

    conn.close()

    # Verifica se o produto existe
    if not product:
        return jsonify({'error': 'Produto não encontrado'}), 404

    # Cria um dicionário com os dados do produto
    product_dict = {
        'id': product[0],
        'name': product[1],
        'quantity': product[2],
        'category_id': product[3],
        'category_name': product[4]
    }

    # Retorna o produto encontrado
    return jsonify(product_dict), 200
