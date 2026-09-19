
failed_attempts = 0
deliveries_processed = 0


def get_valid_input():
    """Keep prompting until the user enters a valid integer or 'quit'."""
    global failed_attempts

    while True:
        user_input = input("Enter stock quantity: ").strip()

        if user_input.lower() == "quit":
            return "quit"

        if user_input.startswith("-") and user_input[1:].isdigit():
            print("Error: Negative quantities are not allowed.")
            failed_attempts += 1
            continue

        # Accept digits 0-9 only; reject blanks, decimals, signs, and text.
        if not user_input.isascii() or not user_input.isdigit():
            print("Error: Invalid input. Please enter a whole number (e.g. 25).")
            failed_attempts += 1
            continue

        try:
            return int(user_input)
        except ValueError:
            # Python may reject an unusually long string of digits.
            print("Error: Quantity is too large. Please enter a smaller number.")
            failed_attempts += 1