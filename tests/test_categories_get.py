import unittest
from unittest.mock import patch, Mock
from flask import Flask
from routes.categories_get import categories_get_routes

class CategoriesGetTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(categories_get_routes)
        self.client = self.app.test_client()

    @patch('sqlite3.connect')
    def test_get_categories(self, mock_connect):
        # Create a mock cursor that fetches some dummy categories
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [(1, 'category1'), (2, 'category2')]

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.get('/categories')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, [{'id': 1, 'name': 'category1'}, {'id': 2, 'name': 'category2'}])

if __name__ == '__main__':
    unittest.main()
