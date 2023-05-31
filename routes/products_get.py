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
    products = [{'id': row[0], 'name': row[1], 'quantity': row[2], 'category_id': row[3]} for row in cursor.fetchall()]

    conn.close()

    # Aplica a paginação aos produtos
    paginator = Pagination(products, page, per_page)
    paginated_products = paginator.paginate()

    # Retorna os produtos paginados
    return jsonify(paginated_products)


# Rota para mostrar um produto específico
@products_get_routes.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT products.id, products.name, products.quantity, products.category_id, categories.name AS category_name
            FROM products
            LEFT JOIN categories ON products.category_id = categories.id
            WHERE products.id = ?
        """, (id,))

        product = cursor.fetchone()

        if product is None:
            return jsonify({'error': 'Produto não encontrado'}), 404

        data = {
            'id': product[0],
            'name': product[1],
            'quantity': product[2],
            'category_id': product[3],
            'category_name': product[4]
        }

        return jsonify(data), 200
    finally:
        conn.close()
