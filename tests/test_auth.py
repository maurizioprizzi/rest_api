import unittest
from flask import Flask
from routes.auth import auth_routes
from flask_jwt_extended import JWTManager

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'super-secret-key'
        self.jwt = JWTManager(self.app)
        self.app.register_blueprint(auth_routes)
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
        auth_response = self.client.post('/auth', json={'email': 'admin@user.com', 'password': '123456'})
        access_token = auth_response.get_json()['access_token']

        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get('/protected', headers=headers)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('message', data)

if __name__ == '__main__':
    unittest.main()
