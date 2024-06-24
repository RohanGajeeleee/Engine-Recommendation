class InputValidator:
    @staticmethod
    def get_valid_input(prompt, allow_empty=False):
        while True:
            user_input = input(prompt).strip()
            if user_input or allow_empty:
                return user_input
            else:
                print("Invalid input. Please enter a valid value.")

    @staticmethod
    def get_valid_price(prompt, allow_empty=False):
        while True:
            price_input = input(prompt).strip()
            if allow_empty and price_input == '':
                return None
            try:
                price = float(price_input)
                if price < 0:
                    raise ValueError("Price cannot be negative.")
                return price
            except ValueError:
                print("Invalid price. Please enter a valid non-negative number.")

    @staticmethod
    def get_valid_availability(prompt, allow_empty=False):
        while True:
            availability_input = input(prompt).strip()
            if allow_empty and availability_input == '':
                return None
            if availability_input == '1':
                return 'Available'
            elif availability_input == '2':
                return 'Unavailable'
            else:
                print("Invalid choice. Please enter 1 for Available or 2 for Unavailable.")

    @staticmethod
    def get_valid_item_id(prompt):
        while True:
            item_id_input = input(prompt).strip()
            try:
                return int(item_id_input)
            except ValueError:
                print("Invalid item ID. Please enter a valid number.")
