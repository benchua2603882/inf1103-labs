import math

from inventory_storage import load_inventory, save_inventory
from product import Product


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


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip().upper()
    if not product_id:
        print("Error: Product ID cannot be empty.")
        return
    if inventory.search_product(product_id) is not None:
        print("Error: Product ID already exists.")
        return
    name = input("Product Name: ").strip()
    if not name:
        print("Error: Product name cannot be empty.")
        return
    price = get_valid_input("Price: ", whole_number=False)
    stock = get_valid_input("Stock Quantity: ")
    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product = inventory.search_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print(f"Name: {product.name}\nCurrent Stock: {product.stock}")
    new_stock = get_valid_input("New Stock Quantity: ")
    product.update_stock(new_stock)
    print("Stock updated successfully!")


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
            inventory.display_all()
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            product = inventory.search_product(input("Enter Product ID: "))
            if product is None:
                print("Product not found.")
            else:
                print("\nProduct Found")
                product.display_information()
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
