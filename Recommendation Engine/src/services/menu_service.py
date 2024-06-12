from src.models.menu_management import MenuItem

class MenuService:
    @staticmethod
    def add_item():
        name = input("Enter item name: ")
        price = float(input("Enter item price: "))
        availability = input("Enter availability (Available/Unavailable): ")
        menu_item = MenuItem(name=name, price=price, availability=availability)
        menu_item.add()
        return True

    @staticmethod
    def update_item():
        item_id = int(input("Enter item ID to update: "))
        name = input("Enter new name (or leave blank to keep current): ")
        price = input("Enter new price (or leave blank to keep current): ")
        availability = input("Enter new availability (or leave blank to keep current): ")
        menu_item = MenuItem(item_id=item_id, name=name if name else None, price=float(price) if price else None, availability=availability if availability else None)
        menu_item.update()
        return True

    @staticmethod
    def delete_item():
        item_id = int(input("Enter item ID to delete: "))
        menu_item = MenuItem(item_id=item_id)
        menu_item.delete()
        return True
