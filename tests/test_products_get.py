import unittest
from unittest.mock import patch, Mock
from flask import Flask
from routes.products_get import products_get_routes

class ProductsGetTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(products_get_routes)
        self.client = self.app.test_client()

    # Teste para obter todos os produtos com sucesso
    @patch('sqlite3.connect')
    def test_get_all_products(self, mock_connect):
        # Cria um cursor fictício que retorna alguns produtos fictícios
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, 'Produto 1', 10, 1, 'Categoria 1'), 
            (2, 'Produto 2', 20, 2, 'Categoria 2')
        ]

        # Faz connect() retornar uma conexão fictícia que retorna o cursor fictício
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.get('/products')
        data = response.get_json()['data']  # Acessa a lista de produtos dentro da chave 'data'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [
            {'id': 1, 'name': 'Produto 1', 'quantity': 10, 'category_id': 1, 'category_name': 'Categoria 1'},
            {'id': 2, 'name': 'Produto 2', 'quantity': 20, 'category_id': 2, 'category_name': 'Categoria 2'}
        ])

    # Teste para obter um produto específico com sucesso
    @patch('sqlite3.connect')
    def test_get_product(self, mock_connect):
        # Cria um cursor fictício que retorna um produto fictício
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, 'Produto 1', 10, 1, 'Categoria 1')

        # Faz connect() retornar uma conexão fictícia que retorna o cursor fictício
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.get('/products/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'id': 1, 'name': 'Produto 1', 'quantity': 10, 'category_id': 1, 'category_name': 'Categoria 1'})

    # Teste para obter um produto que não existe
    @patch('sqlite3.connect')
    def test_get_product_not_found(self, mock_connect):
        # Cria um cursor fictício que não retorna nenhum produto
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None

        # Faz connect() retornar uma conexão fictícia que retorna o cursor fictício
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.get('/products/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {'error': 'Produto não encontrado'})

if __name__ == '__main__':
    unittest.main()
