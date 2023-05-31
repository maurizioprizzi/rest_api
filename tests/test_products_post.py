import unittest
from unittest.mock import patch, Mock
from flask import Flask
from routes.products_post import products_post_routes

class ProductsPostTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(products_post_routes)
        self.client = self.app.test_client()

    @patch('sqlite3.connect')
    def test_create_product(self, mock_connect):
        # Cria um cursor simulado que não retorna nenhum produto existente e
        # retorna um lastrowid de 1 quando um novo produto é inserido
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.lastrowid = 1

        # Faz o connect() retornar uma conexão simulada que retorna nosso cursor simulado
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/products', json={'name': 'novo_produto', 'category_id': 1})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'id': 1, 'name': 'novo_produto', 'quantity': 1, 'category_id': 1, 'category_name': 'Pisos e revestimentos'})

    @patch('sqlite3.connect')
    def test_create_existing_product(self, mock_connect):
        # Cria um cursor simulado que retorna um produto existente
        mock_cursor = Mock()
        mock_cursor.fetchone.side_effect = [(1, 'produto_existente', 2, 1, 'Pisos e revestimentos')]
        mock_cursor.lastrowid = 1

        # Faz o connect() retornar uma conexão simulada que retorna nosso cursor simulado
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/products', json={'name': 'produto_existente', 'category_id': 1})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'id': 1, 'name': 'produto_existente', 'quantity': 3, 'category_id': 1, 'category_name': 'Pisos e revestimentos'})


if __name__ == '__main__':
    unittest.main()
