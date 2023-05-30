# test_users_post.py

import unittest
from unittest.mock import patch, Mock
from flask import Flask
from routes.users_post import users_post_routes

class UsersPostTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(users_post_routes)
        self.client = self.app.test_client()

    @patch('sqlite3.connect')
    def test_register_user(self, mock_connect):
        # Create a mock cursor that fetches no existing user and
        # returns a lastrowid of 1 when a new user is inserted
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_cursor.lastrowid = 1

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/users', json={'email': 'new_user@example.com', 'password': 'new_password'})
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data, {'id': 1, 'email': 'new_user@example.com'})

    @patch('sqlite3.connect')
    def test_register_existing_user(self, mock_connect):
        # Create a mock cursor that fetches an existing user
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1, 'existing_user@example.com', 'existing_password')

        # Make connect() return a mock connection that returns our mock cursor
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        response = self.client.post('/users', json={'email': 'existing_user@example.com', 'password': 'new_password'})
        data = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data, {'error': 'O email fornecido já está registrado'})

if __name__ == '__main__':
    unittest.main()
