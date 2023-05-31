# test_products_get.py

import unittest
from unittest.mock import patch, Mock
from flask import Flask
from routes.products_get import products_get_routes

class ProductsGetTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(products_get_routes)
        self.client = self.app.test_client()

    @patch('sqlite3.connect')
    def test_get_all_products(self, mock_connect):
        # Create a mock cursor that fetches some dummy products
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, 'Product 1', 10, 1, 'Categoria 1'), 
            (2, 'Product 2', 20, 2, 'Categoria 2')
        ]

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.get('/products')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [
            {'id': 1, 'name': 'Product 1', 'quantity': 120, 'category_id': 1, 'category_name': 'Categoria 1'}, 
            {'id': 1, 'name': 'Product 2', 'quantity': 60, 'category_id': 2, 'category_name': 'Categoria 2'}
        ])

    @patch('sqlite3.connect')
    def test_get_product(self, mock_connect):
        # Create a mock cursor that fetches a dummy product
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, 'Product 1', 10, 1, 'Categoria 1')

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.get('/products/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {'id': 1, 'name': 'Product 1', 'quantity': 120, 'category_id': 1, 'category_name': 'Categoria 1'})

    @patch('sqlite3.connect')
    def test_get_product_not_found(self, mock_connect):
        # Create a mock cursor that fetches no product
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.get('/products/1')
        data = response.get_json()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data, {'error': 'Produto não encontrado'})

if __name__ == '__main__':
    unittest.main()
