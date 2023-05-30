from flask import Blueprint, jsonify, request
import sqlite3

# Cria um blueprint para a rota de inserção de categorias
categories_post_routes = Blueprint('categories_post_routes', __name__)

# Rota para inserção de categorias
@categories_post_routes.route('/categories', methods=['POST'])
def create_category():
    try:
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()

        # Obtém o nome da categoria do corpo da solicitação
        data = request.json
        name = data.get('name')

        # Verifica se o nome da categoria já existe no banco de dados
        cursor.execute('SELECT * FROM categories WHERE name = ?', (name,))
        existing_category = cursor.fetchone()

        if existing_category:
            return jsonify({'error': 'Categoria já existente'}), 400

        # Insere a nova categoria no banco de dados
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()

        # Obtém o ID da categoria recém-inserida
        category_id = cursor.lastrowid

        conn.close()

        # Retorna a resposta com o ID da nova categoria
        response = {
            'id': category_id,
            'name': name
        }
        return jsonify(response), 201

    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
