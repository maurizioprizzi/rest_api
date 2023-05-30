import unittest
from unittest.mock import patch, Mock
from flask import Flask
from routes.categories_post import categories_post_routes

class CategoriesPostTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(categories_post_routes)
        self.client = self.app.test_client()

    @patch('sqlite3.connect')
    def test_create_category(self, mock_connect):
        # Create a mock cursor that fetches no existing category and
        # returns a lastrowid of 1 when a new category is inserted
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.lastrowid = 1

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/categories', json={'name': 'new_category'})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'id': 1, 'name': 'new_category'})

    @patch('sqlite3.connect')
    def test_create_existing_category(self, mock_connect):
        # Create a mock cursor that fetches an existing category
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, 'existing_category')

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/categories', json={'name': 'existing_category'})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'Categoria já existente'})

if __name__ == '__main__':
    unittest.main()
