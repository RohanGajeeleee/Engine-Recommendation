import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'client', 'src', 'common')))
from menu_fetcher import MenuFetcher

class TestMenuFetcher(unittest.TestCase):

    def setUp(self):
        self.menu_fetcher = MenuFetcher()

    def test_fetch_item_ids(self):
        result = self.menu_fetcher.fetch_item_ids()
        self.assertIsInstance(result, list)

    def test_fetch_current_menu_items(self):
        result = self.menu_fetcher.fetch_current_menu_items()
        self.assertIsInstance(result, list)

    def test_fetch_item_ids_with_names(self):
        result = self.menu_fetcher.fetch_item_ids_with_names()
        self.assertIsInstance(result, list)

    def test_fetch_current_item_ids_with_names(self):
        result = self.menu_fetcher.fetch_current_item_ids_with_names()
        self.assertIsInstance(result, list)

if __name__ == '__main__':
    unittest.main()
