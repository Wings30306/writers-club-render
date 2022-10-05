import unittest
import app as project
from app import index, login, register, search, all_stories, admin_page, logout
from helper import calculate_age, stories_collection, users_collection, fake_collection, app
import os
from datetime import date, datetime
from flask import url_for, session



class testApp(unittest.TestCase):

    """Set up and tear down"""
    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = project.app.test_client()
 
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
    
    """
    Test suite for app.py
    """
    def test_is_this_thing_on(self):
        self.assertEqual(1, 1)

    def test_env_variables(self):
        database_url = os.getenv("MONGO_URI")
        self.assertEqual(database_url, os.getenv("MONGO_URI"))
        database_name = os.getenv("MONGO_DBNAME")
        self.assertEqual(database_name, os.getenv("MONGO_DBNAME"))
        secret_key = os.getenv("SECRET_KEY")
        self.assertEqual(secret_key, os.getenv("SECRET_KEY"))
    
    def test_database_name_matches_database_url(self):
        database_url = os.getenv("MONGO_URI")
        database_name = os.getenv("MONGO_DBNAME")
        self.assertIn(database_name, database_url)

    def test_calculate_age(self):
        age1 = calculate_age("1984-06-21")
        age2 = calculate_age("2010-11-10")
        age3 = calculate_age(datetime.strftime(date.today(), '%Y-%m-%d'))
        self.assertGreaterEqual(age1, 34)
        self.assertLess(age2, 18)
        self.assertEqual(age3, 0)

    def test_collections(self):
        self.assertIsNotNone(stories_collection)
        self.assertIsNotNone(users_collection)
        self.assertIsNone(fake_collection)

    def test_main_page(self):
        response1 = self.app.get('/')
        response2 = self.app.get('/a')
        self.assertEqual(response1.status_code, 200)
        self.assertNotEqual(response2.status_code, 200)
        

    def test_register_page(self):
        response1 = self.app.get('/register')
        self.assertEqual(response1.status_code, 200)
        response2 = self.app.get('/registration')
        self.assertNotEqual(response2.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login', follow_redirects=False)
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_stories_page(self):
        response = self.app.get('/all-stories', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_admin_page(self):
        response = self.app.get('/admin', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_search_page(self):
        response = self.app.get('/search', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_profile_page(self):
        response1 = self.app.get('/user/wings30306')
        response2 = self.app.get('/user/fake')
        self.assertEqual(response1.status_code, 200)
        self.assertNotEqual(response2.status_code, 200)

if __name__ == "__main__":
    unittest.main()  