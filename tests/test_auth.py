import unittest
from app import app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_authentication(self):
        response = self.app.post('/auth', json={'email': 'admin@user.com', 'password': '123456'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_protected_route_without_authentication(self):
        response = self.app.get('/protected')
        self.assertEqual(response.status_code, 401)

    def test_protected_route_with_authentication(self):
        auth_response = self.app.post('/auth', json={'email': 'admin@user.com', 'password': '123456'})
        access_token = auth_response.json['access_token']
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.app.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json)

if __name__ == '__main__':
    unittest.main()
