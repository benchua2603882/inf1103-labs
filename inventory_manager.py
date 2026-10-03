import json
import math
from pathlib import Path


INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory(filename=INVENTORY_FILE):
    # A new installation starts empty when no saved file exists.
    if not Path(filename).exists():
        print("inventory.json not found. Starting with an empty inventory.")
        return []

    print("inventory.json found.")
    with open(filename, "r", encoding="utf-8") as file:
        inventory = json.load(file)
    validate_inventory(inventory)
    print("Inventory loaded successfully.")
    return inventory


def validate_inventory(inventory):
    # Reject damaged data instead of replacing it with an empty inventory.
    if not isinstance(inventory, list):
        raise ValueError("Inventory must be a list of product dictionaries.")
    product_ids = set()
    for product in inventory:
        if not isinstance(product, dict):
            raise ValueError("Each product must be a dictionary.")
        product_id = product.get("id")
        name = product.get("name")
        price = product.get("price")
        stock = product.get("stock")
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("Each product needs an ID.")
        if product_id.upper() in product_ids:
            raise ValueError("Product IDs must be unique.")
        product_ids.add(product_id.upper())
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Each product needs a name.")
        if type(price) not in (int, float) or not math.isfinite(price) or price < 0:
            raise ValueError("Prices must be finite, non-negative numbers.")
        if type(stock) is not int or stock < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        history = product.get("transaction_history", [stock])
        if not isinstance(history, list) or any(type(value) is not int for value in history):
            raise ValueError("Transaction history must be a list of quantity changes.")
        if sum(history) != stock:
            raise ValueError("Transaction history does not match the current stock.")
        product["transaction_history"] = history


def save_inventory(inventory, filename=INVENTORY_FILE):
    validate_inventory(inventory)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=4, allow_nan=False)
        file.write("\n")


def get_valid_input(prompt, whole_number=True):
    # Reuse the earlier auditor's retry loop for stock quantities and prices.
    while True:
        value = input(prompt).strip()
        try:
            if whole_number:
                if not value.isascii() or not value.isdigit():
                    raise ValueError
                return int(value)
            number = float(value)
            if not math.isfinite(number) or number < 0:
                raise ValueError
            return round(number, 2)
        except ValueError:
            kind = "whole number" if whole_number else "price"
            print(f"Error: Enter a non-negative {kind}.")


def search_product(inventory, product_id):
    for product in inventory:
        if product["id"].upper() == product_id.strip().upper():
            return product
    return None


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Error: Product ID cannot be empty.")
        return
    if search_product(inventory, product_id) is not None:
        print("Error: Product ID already exists.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Error: Product name cannot be empty.")
        return
    price = get_valid_input("Price: ", whole_number=False)
    stock = get_valid_input("Stock Quantity: ")
    inventory.append({
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock,
        "transaction_history": [stock],
    })
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product = search_product(inventory, input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print(f"Name: {product['name']}\nCurrent Stock: {product['stock']}")
    new_stock = get_valid_input("New Stock Quantity: ")
    # The user enters a replacement total; history stores the difference.
    product["transaction_history"].append(new_stock - product["stock"])
    product["stock"] = new_stock
    print("Stock updated successfully!")


def display_all(inventory):
    # Each product is a dictionary; inventory is a list of products.
    print("\nCurrent Inventory")
    print("-" * 60)
    if not inventory:
        print("No products in inventory.")
    for product in inventory:
        print(
            f"ID: {product['id']} | Name: {product['name']} | "
            f"Price: ${product['price']:.2f} | Stock: {product['stock']}"
        )
    print("-" * 60)


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    try:
        inventory = load_inventory()
    except (OSError, ValueError) as error:
        print(f"Unable to load inventory: {error}")
        print("Please fix the saved file before restarting.")
        return

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        option = input("Enter option: ").strip()

        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            product = search_product(inventory, input("Enter Product ID: "))
            if product is None:
                print("Product not found.")
            else:
                print("\nProduct Found")
                display_all([product])
        elif option in ("5", "6"):
            print("Saving inventory before exit..." if option == "6" else "Saving inventory...")
            try:
                save_inventory(inventory)
            except (OSError, ValueError) as error:
                print(f"Unable to save inventory: {error}. Please retry.")
                continue
            print("Inventory saved successfully to inventory.json.")
            if option == "6":
                print("Thank you for using Inventory Management System.")
                break
        else:
            print("Invalid option. Please choose 1 to 6.")


if __name__ == "__main__":
    main()
