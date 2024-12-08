import unittest
from unittest.mock import Mock
import bcrypt
import json
from flask import Flask
from services.admin.movie import *
from services.user.users import *


app = Flask(__name__)
#Testing for addMovie :
class TestDemo(unittest.TestCase):
    def setUp(self):
        self.movieid = 1
        self.moviename = "The Shawshank Redemption"
        self.moviegenre = "Drama"
        self.language = "English"
        self.director = "Frank Darabont"
        self.request = Mock(method='POST')

    def test_demo_success(self):
        with app.app_context():
            response = demo(self.movieid, self.moviename, self.moviegenre, self.language, self.director, self.request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_json(), {"message": "movie added successfully!"})

    def test_demo_missing_params(self):
        with app.app_context():
            response = demo(self.movieid, "", "", "", "", self.request)
            self.assertEqual(response.get_json(), {"message": "All fields are required"})



# #Testing for Registration
class TestRegister(unittest.TestCase):
    def setUp(self):
        self.userid = 1
        self.name = "John Doe"
        self.user = "johndoe"
        self.password = "password123"
        self.usertype = "3"
        self.request = Mock(method='POST')

    def test_register_success(self):
        with app.app_context():
            response = register(self.userid, self.name, self.user, self.password, self.usertype, self.request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'User added successfully!')

    def test_register_existing_user(self):
        with app.app_context():
            # First register the user
            response = register(self.userid, self.name, self.user, self.password, self.usertype, self.request)
            self.assertEqual(response.status_code, 200)

            # Try to register the same user again
            response = register(self.userid, self.name, self.user, self.password, self.usertype, self.request)
            self.assertEqual(response.status_code, 409)
            self.assertEqual(response.data, b'User already exist !')

    def test_register_missing_params(self):
        with app.app_context():
            
            response = register(self.userid, "", "", "", self.request)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.data, b'{"message": " Some Columns are missing or Mispelled the Column name"}')


if __name__ == '__main__':
    unittest.main()
