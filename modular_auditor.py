
failed_attempts = 0
deliveries_processed = 0


def get_valid_input():
    # Keep prompting until the user enters a valid integer or 'quit'.
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

def process_delivery(current_total, new_value):
    # Return the inventory total after adding this delivery.
    return current_total + new_value


def calculate_tax(amount):
    # Return 10% of this delivery amount, as required by the tutorial.
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    #Print the final inventory, successful deliveries, and rejected entries.
    print("\n--- End of Audit ---")
    print(f"Total Units Processed: {total_units}")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    """Coordinate input, delivery processing, tax calculation, and reporting."""
    global failed_attempts, deliveries_processed

    inventory = 0
    failed_attempts = 0
    deliveries_processed = 0

    print("=== Smart Inventory Modular Auditor ===")
    print("Enter daily stock quantities as whole numbers.")
    print("Type 'quit' when you are done.\n")

    while True:
        quantity = get_valid_input()

        if quantity == "quit":
            break

        inventory = process_delivery(inventory, quantity)
        tax = calculate_tax(quantity)
        deliveries_processed += 1

        print(f"Accepted {quantity} units. Current inventory: {inventory}")
        print(f"Tax for this delivery (10%): {tax:.2f}")

        # Keep the original warning, but continue until the user types quit.
        if inventory > 500:
            print("ALERT: Overstock! Inventory exceeds 500 units.")
            break

    generate_report(inventory, failed_attempts)


#run app
main()