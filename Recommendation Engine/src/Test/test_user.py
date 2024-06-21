import unittest
import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.models.user import User
from src.Database.db_config import get_db_connection

class TestUser(unittest.TestCase):
    
    def setUp(self):
        self.user = User('test_id', 'test_name', 'test_password', 'employee')
    
    def tearDown(self):
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM users WHERE employee_id = 'test_id'")
        db.commit()
        cursor.close()
        db.close()

    def test_register_user(self):
        self.user.register()
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE employee_id = 'test_id'")
        result = cursor.fetchone()
        self.assertIsNotNone(result)
        cursor.close()
        db.close()

    def test_authenticate_user(self):
        self.user.register()
        role = User.authenticate('test_id', 'test_password')
        self.assertEqual(role, 'employee')

if __name__ == '__main__':
    unittest.main()
