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
            user_input = input(prompt).strip()
            if not user_input.isdigit():
                print("Invalid item ID. Please enter a valid number.")
            else:
                return int(user_input)
    @staticmethod
    def get_valid_rating(prompt):
        while True:
            rating_input = input(prompt).strip()
            if not rating_input.isdigit() or not (1 <= int(rating_input) <= 5):
                print("Invalid rating. Please enter a number between 1 and 5.")
            else:
                return int(rating_input)
    @staticmethod
    def get_valid_time_of_day(prompt):
        while True:
            time_of_day = input(prompt).strip().lower()
            if time_of_day in ['breakfast', 'lunch', 'dinner']:
                return time_of_day
            else:
                print("Invalid time of day. Please enter 'breakfast', 'lunch', or 'dinner'.")