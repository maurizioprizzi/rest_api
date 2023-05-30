from flask import Blueprint, jsonify, request
import sqlite3

# Cria um blueprint para a rota de adição de produtos ao estoque
inventory_add_routes = Blueprint('inventory_add_routes', __name__)

# Rota para adicionar produtos ao estoque
@inventory_add_routes.route('/inventory/add', methods=['POST'])
def add_to_inventory():
    conn = sqlite3.connect('estoque.db')
    cursor = conn.cursor()

    # Obtém o id do produto e a quantidade do corpo da solicitação
    data = request.json
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    # Verifica se o produto já existe na tabela de produtos
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    existing_product = cursor.fetchone()

    if not existing_product:
        conn.close()
        return jsonify({'error': 'Produto inexistente'}), 404

    # Verifica se o produto já existe no estoque
    cursor.execute('SELECT * FROM inventory WHERE product_id = ?', (product_id,))
    existing_inventory = cursor.fetchone()

    if existing_inventory:
        # Se o produto já existe no estoque, adiciona a quantidade informada ao estoque existente
        new_quantity = existing_inventory[1] + quantity
        cursor.execute('UPDATE inventory SET quantity = ? WHERE product_id = ?', (new_quantity, product_id))
    else:
        # Se o produto não existe no estoque, insere o novo produto com a quantidade informada
        cursor.execute('INSERT INTO inventory (product_id, quantity) VALUES (?, ?)', (product_id, quantity))

    conn.commit()
    conn.close()

    return jsonify({'message': f'Produto {product_id} adicionado ao estoque com sucesso.'}), 200
