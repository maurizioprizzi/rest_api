import pytest
from flask import Flask
from flask_jwt_extended import JWTManager

# Cria uma instância do Flask para os testes
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        # Cria uma instância do aplicativo Flask
        self.app = Flask(__name__)
        self.app.register_blueprint(auth_routes)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_authentication(self):
        response = self.client.post('/auth', json={'email': 'admin@user.com', 'password': '123456'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    def test_protected_route_without_authentication(self):
        response = self.client.get('/protected')
        self.assertEqual(response.status_code, 401)

    def test_protected_route_with_authentication(self):
        # Simula a autenticação obtendo o token de acesso
        auth_response = self.client.post('/auth', json={'email': 'admin@user.com', 'password': '123456'})
        access_token = auth_response.get_json()['access_token']

        # Faz a chamada à rota protegida incluindo o token de acesso no cabeçalho
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/protected', headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()
