import math

from inventory_storage import load_inventory, save_inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from inventory import Inventory
from order import Order


def create_order(inventory: Inventory, orders: dict[str, Order]) -> None:
    # Orders are kept for this run; inventory saving still only saves products.
    order_id = input("Order ID: ").strip().upper()
    if not order_id or order_id in orders:
        print("Please enter a new, non-empty order ID.")
        return
    order = Order(order_id)
    orders[order_id] = order
    while True:
        product_id = input("Product ID (or 'done' to finish): ").strip()
        if product_id.lower() == "done":
            break
        product = inventory.find_product(product_id)
        if product is None:
            print("Product not found.")
            continue
        quantity = get_valid_input("Order quantity: ")
        try:
            order.add_order_line(product, quantity)
            print("Order line added.")
        except ValueError as error:
            print(error)
    order.display_information()


def display_orders(orders: dict[str, Order]) -> None:
    # Each order is responsible for displaying its own lines and total.
    if not orders:
        print("No orders in this session.")
    for order in orders.values():
        order.display_information()


def remove_order_line(orders: dict[str, Order]) -> None:
    order = orders.get(input("Order ID: ").strip().upper())
    if order is None:
        print("Order not found.")
        return
    order.display_information()
    line_number = get_valid_input("Line number to remove: ")
    try:
        order.remove_order_line(line_number)
        print("Order line removed.")
    except ValueError as error:
        print(error)


def get_supplier(inventory: Inventory) -> Supplier:
    # Reuse an existing supplier, or ask for the details of a new one.
    while True:
        supplier_id = input("Supplier ID: ").strip().upper()
        if not supplier_id:
            print("Supplier ID cannot be empty.")
            continue
        for product in inventory.get_products():
            if product.supplier.supplier_id == supplier_id:
                print(f"Using supplier: {product.supplier.name}")
                return product.supplier
        name = input("Supplier name: ").strip()
        email = input("Supplier email: ").strip()
        try:
            return Supplier(supplier_id, name, email)
        except ValueError as error:
            print(error)


def get_valid_input(prompt, whole_number=True):
    # Keep asking until a valid non-negative number is entered.
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
            return number
        except ValueError:
            kind = "whole number" if whole_number else "number"
            print(f"Error: Enter a non-negative {kind}.")


def add_product(inventory):
    # Collect the chosen product type and its details, then add the new object.
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")
    while True:
        product_type = input("Choose product type (1 or 2): ").strip()
        if product_type in ("1", "2"):
            break
        print("Invalid product type. Please choose 1 or 2.")
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
    price = round(get_valid_input("Price: ", whole_number=False), 2)
    stock = get_valid_input("Stock Quantity: ")
    supplier = get_supplier(inventory)
    if product_type == "1":
        weight = get_valid_input("Weight (kg): ", whole_number=False)
        product = PhysicalProduct(product_id, name, price, stock, weight, supplier)
    else:
        download_size = get_valid_input("Download size (MB): ", whole_number=False)
        product = DigitalProduct(product_id, name, price, stock, download_size, supplier)
    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory):
    # Find the product and ask it to update its stock with the user's new quantity.
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
    # Load saved products, run the menu, and save the inventory before exiting.
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    try:
        inventory = load_inventory()
    except (OSError, ValueError) as error:
        print(f"Unable to load inventory: {error}")
        print("Please fix the saved file before restarting.")
        return

    orders: dict[str, Order] = {}
    print("Orders last for this session only and do not change stock.")
    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("7. Create Order")
        print("8. Display Orders")
        print("9. Remove Order Line")
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
        elif option == "7":
            create_order(inventory, orders)
        elif option == "8":
            display_orders(orders)
        elif option == "9":
            remove_order_line(orders)
        else:
            print("Invalid option. Please choose 1 to 9.")


if __name__ == "__main__":
    main()
