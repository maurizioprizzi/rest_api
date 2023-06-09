import unittest
from unittest.mock import patch
from flask import Flask
from routes.categories_get import get_categories
import sqlite3

class CategoriesGetTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.add_url_rule('/categories', 'get_categories', get_categories)
        self.client = self.app.test_client()

    # Teste para obter as categorias com sucesso
    @patch('routes.categories_get.sqlite3.connect')
    def test_get_categories(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'name': 'category1'},
            {'id': 2, 'name': 'category2'}
        ]

        response = self.client.get('/categories')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [{'id': 1, 'name': 'category1'}, {'id': 2, 'name': 'category2'}])

    # Teste para obter as categorias quando está vazio
    @patch('routes.categories_get.sqlite3.connect')
    def test_get_categories_empty(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        mock_cursor.fetchall.return_value = []

        response = self.client.get('/categories')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [])

    # Teste para obter as categorias com erro no banco de dados
    @patch('routes.categories_get.sqlite3.connect')
    def test_get_categories_db_error(self, mock_connect):
        mock_connect.side_effect = sqlite3.Error("Não foi possível estabelecer uma conexão com o banco de dados")

        response = self.client.get('/categories')
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data, {'error': 'Não foi possível estabelecer uma conexão com o banco de dados'})


if __name__ == '__main__':
    unittest.main()
