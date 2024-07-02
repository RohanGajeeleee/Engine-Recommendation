from common.menu_fetcher import MenuFetcher
from common.choice_fetcher import ChoiceFetcher
from common.menu_validator import MenuValidator
from common.menu_utils import MenuUtils

class MenuItemChecker:
    fetch_item_ids = MenuFetcher.fetch_item_ids
    fetch_current_menu_items = MenuFetcher.fetch_current_menu_items
    fetch_item_ids_with_names = MenuFetcher.fetch_item_ids_with_names
    fetch_current_item_ids_with_names = MenuFetcher.fetch_current_item_ids_with_names
    fetch_user_choices = ChoiceFetcher.fetch_user_choices

    get_existing_item_id = lambda prompt: MenuValidator.get_existing_item_id(prompt, MenuFetcher.fetch_item_ids_with_names)
    get_existing_choice_id = MenuValidator.get_existing_choice_id
    get_existing_current_item_id = lambda prompt: MenuValidator.get_existing_current_item_id(prompt, MenuFetcher.fetch_current_item_ids_with_names)

    parse_available_items = MenuUtils.parse_available_items
    is_item_available = MenuUtils.is_item_available
