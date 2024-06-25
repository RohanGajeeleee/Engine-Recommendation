# client/src/common/menu_utils.py

class MenuUtils:
    @staticmethod
    def parse_available_items(view_response):
        items = view_response.split('\n')
        available_items = set()
        for item in items:
            if "Availability: Available" in item:
                item_id = int(item.split(",")[0].split(":")[1].strip())
                available_items.add(item_id)
        return available_items

    @staticmethod
    def is_item_available(item_id, available_items):
        return item_id in available_items
