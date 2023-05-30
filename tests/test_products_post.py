# test_products_post.py

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
        # Create a mock cursor that fetches no existing product and
        # returns a lastrowid of 1 when a new product is inserted
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.lastrowid = 1

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/products', json={'name': 'new_product', 'category_id': 1})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'id': 1, 'name': 'new_product', 'quantity': 1, 'category_id': 1, 'category_name': 'category1'})

    @patch('sqlite3.connect')
    def test_create_existing_product(self, mock_connect):
        # Create a mock cursor that fetches an existing product
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, 'existing_product', 2, 1, 'category1')

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/products', json={'name': 'existing_product', 'category_id': 1})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'O produto fornecido já existe'})

if __name__ == '__main__':
    unittest.main()
