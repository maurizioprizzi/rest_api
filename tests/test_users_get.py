import unittest
from unittest.mock import patch, Mock
from flask import Flask
from routes.users_get import users_get_routes

class UsersGetTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(users_get_routes)
        self.client = self.app.test_client()

    @patch('utils.pagination.Pagination')
    @patch('sqlite3.connect')
    def test_get_all_users(self, mock_connect, mock_pagination):
        # Cria um cursor mock que retorna alguns usuários fictícios
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (1, 'user1@example.com', 'password1'), 
            (2, 'user2@example.com', 'password2')
        ]

        # Faz com que connect() retorne uma conexão mock que retorna nosso cursor mock
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn

        # Faz com que o paginate retorne os usuários diretamente
        mock_pagination_instance = Mock()
        mock_pagination_instance.paginate.return_value = {
            'data': [
                {'id': 1, 'email': 'user1@example.com', 'password': 'password1'},
                {'id': 2, 'email': 'user2@example.com', 'password': 'password2'}
            ]
        }
        mock_pagination.return_value = mock_pagination_instance

        response = self.client.get('/users')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data, {
            'data': [
                {'id': 1, 'email': 'user1@example.com', 'password': 'password1'},
                {'id': 2, 'email': 'user2@example.com', 'password': 'password2'}
            ]
        })

if __name__ == '__main__':
    unittest.main()
