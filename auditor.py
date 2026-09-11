"""
Smart Inventory Auditor
Lab tutorial: loops, if/elif/else, input validation, and running state.
"""

# 1. Initialize inventory (and a reject counter for the final report)
inventory = 0
rejected_entries = 0

print("=== Smart Inventory Auditor ===")
print("Enter daily stock quantities as whole numbers.")
print("Type 'quit' when you are done.\n")

# 2. Continuous loop until the user types quit (or overstock forces a stop)
while True:
    user_input = input("Enter stock quantity: ").strip()

    # Exit path — report is printed after the loop
    if user_input.lower() == "quit":
        break

    # 4. Handle invalid input (text such as "ten", blanks, decimals, etc.)
    #    isdigit() is True only for strings of 0-9 with no sign or decimal.
    # 5. Negatives fail isdigit() as well ("-10".isdigit() == False),
    #    so we give them a clearer business-rule message first.
    if user_input.startswith("-") and user_input[1:].isdigit():
        print("Error: Negative quantities are not allowed.")
        rejected_entries += 1
        continue

    if not user_input.isdigit():
        print("Error: Invalid input. Please enter a whole number (e.g. 25).")
        rejected_entries += 1
        continue

    # 3. Accept the value as an integer
    quantity = int(user_input)

    # 6. Keep a running total
    inventory += quantity
    print(f"Accepted {quantity} units. Current inventory: {inventory}")

    # 7. Overstock alert — stop immediately if capacity is exceeded
    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units. Stopping.")
        break

# 8. Reporting (runs after quit OR after an overstock break)
print("\n--- End of Audit ---")
print(f"Total Units Processed: {inventory}")
print(f"Number of Failed/Rejected Entries: {rejected_entries}")