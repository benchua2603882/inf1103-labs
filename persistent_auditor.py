failed_attempts = 0
deliveries_processed = 0


def load_inventory():
    # Load the previously saved inventory total and transaction history.
    # If inventory.txt does not exist, start with an empty inventory and history.
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

        inventory = 0
        transaction_history = []

        if len(lines) >= 1:
            inventory = int(lines[0].replace("Inventory:", "").strip())

        if len(lines) >= 2:
            history_data = lines[1].replace("Transaction History:", "").strip()

            if history_data:
                transaction_history = [
                    int(value.strip())
                    for value in history_data.split(",")
                    if value.strip()
                ]

        return inventory, transaction_history

    except FileNotFoundError:
        return 0, []
    except (ValueError, OSError):
        # If the saved file cannot be read correctly, start safely from empty data.
        print("Warning: inventory.txt could not be loaded. Starting with empty inventory.")
        return 0, []


def save_inventory(inventory, transaction_history):
    # Save the final inventory total and every valid transaction amount.
    with open("inventory.txt", "w") as file:
        file.write(f"Inventory: {inventory}\n")
        file.write("Transaction History: ")
        file.write(",".join(str(value) for value in transaction_history))
        file.write("\n")


def get_valid_input():
    # Keep prompting until the user enters a valid integer or 'quit'.
    global failed_attempts

    while True:
        user_input = input("Enter Quantity: ").strip()

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


def process_delivery(current_total, new_value):
    # Return the inventory total after adding this delivery.
    return current_total + new_value


def calculate_tax(amount):
    # Return 10% of this delivery amount, as required by the tutorial.
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    # Print the final inventory, successful deliveries, and rejected entries.
    print("\n--- End of Audit ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    """Coordinate input, delivery processing, tax calculation, and reporting."""
    global failed_attempts, deliveries_processed

    inventory, transaction_history = load_inventory()
    failed_attempts = 0
    deliveries_processed = len(transaction_history)

    print("=== Smart Inventory Modular Auditor ===")
    print("Enter daily stock quantities as whole numbers.")
    print("Type 'quit' when you are done.")
    print(f"Starting inventory: {inventory}\n")

    while True:
        product_name = input("Enter Product Name: ").strip()

        if product_name.lower() == "quit":
            save_inventory(inventory, transaction_history)
            print("Inventory and transaction history saved to inventory.txt.")
            break

        while not product_name:
            print("Error: Product name cannot be empty.")
            product_name = input("Enter Product Name: ").strip()

            if product_name.lower() == "quit":
                save_inventory(inventory, transaction_history)
                print("Inventory and transaction history saved to inventory.txt.")
                generate_report(inventory, failed_attempts)
                return

        quantity = get_valid_input()

        if quantity == "quit":
            save_inventory(inventory, transaction_history)
            print("Inventory and transaction history saved to inventory.txt.")
            break

        inventory = process_delivery(inventory, quantity)
        transaction_history.append(quantity)
        tax = calculate_tax(quantity)
        deliveries_processed += 1

        print("\nNew Delivery Added:")
        print(f"Product Name: {product_name}")
        print(f"Quantity: {quantity}")
        print(f"Current inventory: {inventory}")
        print(f"Tax for this delivery (10%): {tax:.2f}")

        # Keep the original warning, but continue until the user types quit.
        if inventory > 500:
            print("ALERT: Overstock! Inventory exceeds 500 units.")

    generate_report(inventory, failed_attempts)


# run app
main()
