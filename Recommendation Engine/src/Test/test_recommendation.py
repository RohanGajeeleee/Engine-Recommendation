import unittest
import sys
import os

# Ensure the src directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.models.recommendations import Recommendation
from src.Database.db_config import get_db_connection



class TestRecommendation(unittest.TestCase):
    def setUp(self):
        self.db = get_db_connection()
        self.cursor = self.db.cursor()
        
        # Clear existing data
        self.cursor.execute("DELETE FROM menu")
        self.cursor.execute("DELETE FROM feedback")
        self.cursor.execute("DELETE FROM choices")
        self.cursor.execute("DELETE FROM current_menu")
        self.cursor.execute("DELETE FROM next_day_menu")
        self.cursor.execute("DELETE FROM users")
        
        # Insert sample data
        self.cursor.execute("INSERT INTO menu (id, name, price, availability) VALUES (1, 'Test Dish 1', 10.00, 'Available')")
        self.cursor.execute("INSERT INTO menu (id, name, price, availability) VALUES (2, 'Test Dish 2', 15.00, 'Available')")
        self.cursor.execute("INSERT INTO menu (id, name, price, availability) VALUES (3, 'Test Dish 3', 20.00, 'Available')")
        self.cursor.execute("INSERT INTO menu (id, name, price, availability) VALUES (4, 'Test Dish 4', 25.00, 'Available')")
        self.cursor.execute("INSERT INTO menu (id, name, price, availability) VALUES (5, 'Test Dish 5', 30.00, 'Available')")
        
        # Insert user
        self.cursor.execute("INSERT INTO users (employee_id, name, password, role) VALUES ('test_emp', 'Test Employee', 'password', 'employee')")
        
        self.db.commit()

    def tearDown(self):
        self.cursor.close()
        self.db.close()

    def test_fetch_available_menu_items(self):
        items = Recommendation.fetch_available_menu_items()
        self.assertEqual(len(items), 5)  # Expecting 5 items to be available

    def test_recommend_items_for_next_day_no_feedback(self):
        recommendations = Recommendation.recommend_items_for_next_day()
        print("Test Recommend No Feedback:", recommendations)
        self.assertEqual(len(recommendations), 5)  # All items should be recommended since there's no feedback

if __name__ == '__main__':
    unittest.main()
