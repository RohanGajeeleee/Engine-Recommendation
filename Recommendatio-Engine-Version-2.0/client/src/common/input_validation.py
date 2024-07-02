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
    def get_valid_number(prompt):
        while True:
            try:
                num = int(input(prompt))
                if num > 0:
                    return num
                else:
                    print("Please enter a positive number.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

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

    @staticmethod
    def get_valid_choice(prompt, options, allow_empty=False):
        while True:
            print(prompt)
            for key, value in options.items():
                print(f"{key}: {value}")
            choice = input("Enter choice (or leave blank to keep current): ").strip()
            if allow_empty and not choice:
                return None
            if choice in options:
                return options[choice]
            print("Invalid choice. Please try again.")

    @staticmethod
    def get_valid_availability(prompt, allow_empty=False):
        options = {"1": "Available", "2": "Unavailable"}
        return InputValidator.get_valid_choice(prompt, options, allow_empty)

    @staticmethod
    def get_valid_spice_level(prompt, allow_empty=False):
        options = {"1": "Low", "2": "Medium", "3": "High"}
        return InputValidator.get_valid_choice(prompt, options, allow_empty)

    @staticmethod
    def get_valid_food_category(prompt, allow_empty=False):
        options = {"1": "North-Indian", "2": "South-Indian", "3": "Other", "4": "Dessert"}
        return InputValidator.get_valid_choice(prompt, options, allow_empty)

    @staticmethod
    def get_valid_dietary_type(prompt, allow_empty=False):
        options = {"1": "Vegetarian", "2": "Non-Vegetarian", "3": "Eggetarian"}
        return InputValidator.get_valid_choice(prompt, options, allow_empty)

    @staticmethod
    def get_valid_sweet_tooth(prompt, allow_empty=False):
        options = {"1": "Yes", "2": "No"}
        return InputValidator.get_valid_choice(prompt, options, allow_empty)

    @staticmethod
    def get_valid_role(prompt, allow_empty=False):
        options = {"1": "admin", "2": "chef", "3":"employee"}
        return InputValidator.get_valid_choice(prompt, options, allow_empty)
