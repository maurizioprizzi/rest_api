from flask import Blueprint, jsonify, current_app
import sqlite3
from sqlite3 import Error
import logging

# Cria um blueprint para as rotas de obtenção de categorias
categories_get_routes = Blueprint('categories_get_routes', __name__)

# Função para obter uma conexão com o banco de dados
def get_db_connection():
    try:
        # Estabelece uma conexão com o banco de dados SQLite
        conn = sqlite3.connect('estoque.db')
        # Define o tipo de retorno das linhas como dicionário
        conn.row_factory = sqlite3.Row
        return conn, None
    except Error as e:
        logging.error(str(e))
        return None, "Não foi possível estabelecer uma conexão com o banco de dados"

# Função para obter as categorias do banco de dados
def get_categories_db():
    conn, error = get_db_connection()
    if conn is None:
        return None, error, 500
    
    cursor = conn.cursor()
    try:
        # Executa uma consulta para obter todas as categorias
        cursor.execute('SELECT * FROM categories')
        rows = cursor.fetchall()

        categories = []
        # Converte as linhas em uma lista de dicionários
        for row in rows:
            categories.append({'id': row['id'], 'name': row['name']})

        return categories, None, 200
    except Error as e:
        logging.error(str(e))
        return None, str(e), 500
    finally:
        # Fecha a conexão com o banco de dados
        conn.close()

# Rota para obter as categorias
@categories_get_routes.route('/categories', methods=['GET'])
def get_categories():
    # Chama a função para obter as categorias do banco de dados
    categories, error, status_code = get_categories_db()
    if categories is None:
        # Se ocorrer um erro, retorna uma resposta com o erro e o código de status apropriado
        return jsonify({'error': error}), status_code
    else:
        # Se obtiver as categorias com sucesso, retorna as categorias e o código de status apropriado
        return jsonify(categories), status_code
