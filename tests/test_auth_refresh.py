import unittest
from flask import Flask
from routes.auth import auth_routes
from routes.auth_refresh import auth_refresh_routes
from flask_jwt_extended import JWTManager

class AuthRefreshTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret-key'
        self.jwt = JWTManager(self.app)
        self.app.register_blueprint(auth_routes)
        self.app.register_blueprint(auth_refresh_routes)
        self.client = self.app.test_client()

    def test_refresh_route_without_authentication(self):
        response = self.client.post('/auth/refresh')
        self.assertEqual(response.status_code, 401)

    def test_refresh_route_with_authentication(self):
        # Simula a autenticação obtendo o token de acesso
        auth_response = self.client.post('/auth', json={'email': 'admin@user.com', 'password': '123456'})
        access_token = auth_response.get_json()['access_token']

        # Faz a chamada à rota de renovação incluindo o token de acesso no cabeçalho
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.post('/auth/refresh', headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)

if __name__ == '__main__':
    unittest.main()
