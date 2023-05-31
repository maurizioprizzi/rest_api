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
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None

        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/products', json={'name': 'Produto Teste', 'quantity': 10, 'category_id': 1})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'message': 'Produto criado com sucesso'})

        mock_conn.commit.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('sqlite3.connect')
    def test_create_existing_product(self, mock_connect):
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)

        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/products', json={'name': 'Produto Teste', 'quantity': 10, 'category_id': 1})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Produto já existe'})

        mock_conn.commit.assert_not_called()
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
