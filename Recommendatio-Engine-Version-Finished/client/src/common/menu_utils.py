import logging

class MenuUtils:
    def parse_available_items(self, menu_items):
        try:
            items = menu_items.split('\n')
            available_items = []
            for item in items:
                if item.startswith("ID:"):
                    parts = item.split(', ')
                    item_id = int(parts[0].split(':')[1].strip())
                    item_name = parts[1].split(':')[1].strip()
                    availability = parts[3].split(':')[1].strip()
                    if availability == 'Available':
                        available_items.append({'id': item_id, 'name': item_name})
            return available_items
        except Exception as e:
            logging.error(f"Error parsing available items: {e}")
            return []

    def is_item_available(self, available_items, item_id):
        for item in available_items:
            if item['id'] == item_id:
                return True
        return False
