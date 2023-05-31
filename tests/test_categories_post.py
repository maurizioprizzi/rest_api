import unittest
from unittest.mock import patch, Mock
from flask import Flask
from routes.categories_post import categories_post_routes

class CategoriesPostTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(categories_post_routes)
        self.client = self.app.test_client()

    # Teste para criar uma nova categoria com sucesso
    @patch('sqlite3.connect')
    def test_create_category(self, mock_connect):
        # Cria um cursor fictício que não retorna nenhuma categoria existente
        # e define um lastrowid de 1 quando uma nova categoria é inserida
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.lastrowid = 1

        # Faz connect() retornar uma conexão fictícia que retorna o cursor fictício
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/categories', json={'name': 'new_category'})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'id': 1, 'name': 'new_category'})

    # Teste para criar uma categoria existente
    @patch('sqlite3.connect')
    def test_create_existing_category(self, mock_connect):
        # Cria um cursor fictício que retorna uma categoria existente
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, 'existing_category')

        # Faz connect() retornar uma conexão fictícia que retorna o cursor fictício
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/categories', json={'name': 'existing_category'})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Categoria já existente'})

if __name__ == '__main__':
    unittest.main()
