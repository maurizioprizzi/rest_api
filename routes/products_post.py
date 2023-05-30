from flask import Blueprint, jsonify, request
import sqlite3

# Cria um blueprint para a rota de inserção de produtos
products_post_routes = Blueprint('products_post_routes', __name__)

# Rota para inserção de produtos
@products_post_routes.route('/products', methods=['POST'])
def create_product():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Obtém os dados do produto do corpo da solicitação
    data = request.json
    name = data.get('name')
    category_id = data.get('category_id')

    # Verifica se o nome do produto foi fornecido
    if not name:
        conn.close()
        return jsonify({'error': 'O nome do produto é obrigatório'}), 400

    # Verifica se a categoria existe no banco de dados
    cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
    existing_category = cursor.fetchone()

    if not existing_category:
        conn.close()
        return jsonify({'error': 'A categoria fornecida não existe'}), 400

    # Verifica se o produto já existe para a categoria fornecida
    cursor.execute('SELECT * FROM products WHERE name = ? AND category_id = ?', (name, category_id))
    existing_product = cursor.fetchone()

    if existing_product:
        # Se o produto já existe, incrementa a quantidade
        new_quantity = existing_product[2] + 1
        product_id = existing_product[0]
        cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_quantity, product_id))
    else:
        # Se o produto não existe, insere-o no banco de dados
        cursor.execute('''
            INSERT INTO products (name, quantity, category_id, category_name)
            VALUES (?, 1, ?, ?)
        ''', (name, category_id, existing_category[1]))

    conn.commit()

    # Obtém o ID do produto recém-inserido
    if existing_product:
        product_id = existing_product[0]
    else:
        product_id = cursor.lastrowid

    conn.close()

    # Retorna a resposta com o ID do novo produto
    response = {
        'id': product_id,
        'name': name,
        'quantity': new_quantity if existing_product else 1,
        'category_id': category_id,
        'category_name': existing_category[1]
    }
    return jsonify(response), 201
