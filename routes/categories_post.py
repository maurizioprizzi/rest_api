from flask import Blueprint, jsonify, request
import sqlite3

# Cria um blueprint para as rotas de criação de categorias
categories_post_routes = Blueprint('categories_post_routes', __name__)

# Rota para criar uma nova categoria
@categories_post_routes.route('/categories', methods=['POST'])
def create_category():
    conn = None
    try:
        # Estabelece uma conexão com o banco de dados SQLite
        conn = sqlite3.connect('estoque.db')
        cursor = conn.cursor()

        # Obtém os dados da requisição JSON
        data = request.get_json()
        name = data.get('name', None)
        if not name:
            # Retorna um erro se o nome da categoria não for fornecido
            return jsonify({'error': 'Nome de categoria necessário'}), 400

        # Verifica se a categoria já existe no banco de dados
        cursor.execute('SELECT * FROM categories WHERE name = ?', (name,))
        existing_category = cursor.fetchone()
        if existing_category:
            # Retorna um erro se a categoria já existir
            return jsonify({'error': 'Categoria já existente'}), 400

        # Insere a nova categoria no banco de dados
        cursor.execute('INSERT INTO categories (name) VALUES (?)', (name,))
        conn.commit()
        category_id = cursor.lastrowid

        # Retorna os detalhes da nova categoria
        return jsonify({'id': category_id, 'name': name}), 201

    except sqlite3.Error as e:
        # Retorna um erro se ocorrer um erro no banco de dados
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        # Retorna um erro genérico se ocorrer um erro desconhecido
        return jsonify({'error': 'Erro desconhecido: {}'.format(str(e))}), 500
    finally:
        if conn:
            # Fecha a conexão com o banco de dados
            conn.close()
