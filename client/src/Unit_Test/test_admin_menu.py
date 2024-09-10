import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import unittest
from unittest.mock import patch, MagicMock
from src.presentation.admin_menu import AdminMenu
from src.presentation.menu_manager import MenuManager

class TestAdminMenu(unittest.TestCase):

    @patch('src.presentation.admin_menu.MenuManager')
    def setUp(self, MockMenuManager):
        self.menu_manager = MockMenuManager.return_value
        self.admin_menu = AdminMenu()

    @patch('src.common.input_validation.InputValidator')
    @patch('src.common.menu_item_checker.MenuItemChecker')
    def test_add_menu_item_valid_input(self, MockMenuItemChecker, MockInputValidator):
        MockInputValidator.return_value.get_valid_input.return_value = "Paneer Butter Masala"
        MockInputValidator.return_value.get_valid_price.return_value = "250.00"
        MockInputValidator.return_value.get_valid_availability.return_value = "1"
        MockInputValidator.return_value.get_valid_spice_level.return_value = "2"
        MockInputValidator.return_value.get_valid_food_category.return_value = "1"
        MockInputValidator.return_value.get_valid_dietary_type.return_value = "1"

        with patch('builtins.input', return_value='1'):
            result = self.admin_menu.handle_choice('1')
            self.menu_manager.add_item.assert_called_once()
            self.assertTrue(result)

    @patch('src.common.input_validation.InputValidator')
    @patch('src.common.menu_item_checker.MenuItemChecker')
    def test_update_menu_item_valid_input(self, MockMenuItemChecker, MockInputValidator):
        MockMenuItemChecker.return_value.get_existing_item_id.return_value = "1"

        MockInputValidator.return_value.get_valid_input.return_value = "Paneer Tikka"
        MockInputValidator.return_value.get_valid_price.return_value = "300.00"
        MockInputValidator.return_value.get_valid_availability.return_value = "2"
        MockInputValidator.return_value.get_valid_spice_level.return_value = "3"
        MockInputValidator.return_value.get_valid_food_category.return_value = "1"
        MockInputValidator.return_value.get_valid_dietary_type.return_value = "1"

        with patch('builtins.input', return_value='2'):
            result = self.admin_menu.handle_choice('2')
            self.menu_manager.update_item.assert_called_once()
            self.assertTrue(result)

    @patch('src.common.input_validation.InputValidator')
    @patch('src.common.menu_item_checker.MenuItemChecker')
    def test_delete_menu_item_valid_input(self, MockMenuItemChecker, MockInputValidator):
        MockMenuItemChecker.return_value.get_existing_item_id.return_value = "1"

        with patch('builtins.input', return_value='3'):
            result = self.admin_menu.handle_choice('3')
            self.menu_manager.delete_item.assert_called_once()
            self.assertTrue(result)

    @patch('src.common.input_validation.InputValidator')
    @patch('src.common.menu_item_checker.MenuItemChecker')
    def test_view_menu(self, MockMenuItemChecker, MockInputValidator):
        self.menu_manager.view_menu.return_value = True
        
        with patch('builtins.input', return_value='4'):
            result = self.admin_menu.handle_choice('4')
            self.menu_manager.view_menu.assert_called_once()
            self.assertTrue(result)

    def test_invalid_choice(self):
        with patch('builtins.input', return_value='invalid'):
            result = self.admin_menu.handle_choice('invalid')
            self.assertTrue(result)

    def test_logout(self):
        with patch('builtins.input', return_value='5'):
            result = self.admin_menu.handle_choice('5')
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
