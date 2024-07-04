import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'client', 'src')))
from common.menu_item_checker import MenuItemChecker

class TestMenuItemChecker(unittest.TestCase):

    def setUp(self):
        self.menu_item_checker = MenuItemChecker()

    def test_fetch_item_ids(self):
        result = self.menu_item_checker.fetch_item_ids()
        self.assertIsInstance(result, list)

    def test_fetch_current_menu_items(self):
        result = self.menu_item_checker.fetch_current_menu_items()
        self.assertIsInstance(result, list)

    def test_fetch_item_ids_with_names(self):
        result = self.menu_item_checker.fetch_item_ids_with_names()
        self.assertIsInstance(result, list)

    def test_fetch_current_item_ids_with_names(self):
        result = self.menu_item_checker.fetch_current_item_ids_with_names()
        self.assertIsInstance(result, list)

if __name__ == '__main__':
    unittest.main()
