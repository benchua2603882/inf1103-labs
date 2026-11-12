import math

from inventory_storage import load_inventory, save_inventory
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier
from inventory import Inventory
from order import Order
from product import Product
from discount_strategy import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount


def show_product_details(product: Product) -> None:
    # Use the same calls for any Product, without checking its subclass.
    product.display_information()
    print(product.get_fulfilment_info())


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
        quantity = int(get_valid_input("Order quantity: "))
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


def change_order_discount(orders: dict[str, Order]) -> None:
    # Choose a strategy here; Order only needs to know its apply() method.
    order = orders.get(input("Order ID: ").strip().upper())
    if order is None:
        print("Order not found.")
        return
    while True:
        print("1. No discount\n2. Percentage discount\n3. Bulk discount\n4. Student discount (5%)")
        choice = input("Choose discount (1 to 4): ").strip()
        try:
            if choice == "1":
                order.set_discount(NoDiscount())
            elif choice == "2":
                percentage = get_valid_input("Percentage: ", whole_number=False)
                order.set_discount(PercentageDiscount(percentage))
            elif choice == "3":
                threshold = get_valid_input("Minimum order total: ", whole_number=False)
                amount = get_valid_input("Amount to take off: ", whole_number=False)
                order.set_discount(BulkDiscount(threshold, amount))
            elif choice == "4":
                order.set_discount(StudentDiscount())
            else:
                print("Invalid discount. Please choose 1 to 4.")
                continue
        except ValueError as error:
            print(error)
            continue
        print("Order discount updated.")
        order.display_information()
        return


def remove_order_line(orders: dict[str, Order]) -> None:
    order = orders.get(input("Order ID: ").strip().upper())
    if order is None:
        print("Order not found.")
        return
    order.display_information()
    line_number = int(get_valid_input("Line number to remove: "))
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


def get_valid_input(prompt: str, whole_number: bool = True) -> int | float:
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


def get_positive_float(prompt: str) -> float:
    # Keep asking for a price until it is a finite number above zero.
    while True:
        try:
            value = float(input(prompt))
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")
            continue
        if not math.isfinite(value):
            print("Please enter a finite number.")
            continue
        if value <= 0:
            print("Please enter a number greater than zero.")
            continue
        return value


def import_products(inventory: Inventory) -> None:
    # Ask which supplier to share between the products in this CSV.
    path = input("CSV path (Enter for products.csv): ").strip() or "products.csv"
    supplier = get_supplier(inventory)
    print("CSV products use 0 for weight or download size because these columns are not provided.")
    load_products(path, inventory, supplier)


def add_product(inventory: Inventory) -> None:
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
    price = get_positive_float("Price: ")
    stock = int(get_valid_input("Stock Quantity: "))
    supplier = get_supplier(inventory)
    weight = 0.0
    download_size = 0.0
    if product_type == "1":
        weight = get_valid_input("Weight (kg): ", whole_number=False)
        product_type = "physical"
    else:
        download_size = get_valid_input("Download size (MB): ", whole_number=False)
        product_type = "digital"
    # Ask the factory to build the product after collecting its details.
    product = ProductFactory.create(
        product_type, product_id, name, price, stock, supplier,
        weight=weight, download_size=download_size,
    )
    inventory.add_product(product)
    print("Product added successfully!")


def update_stock(inventory: Inventory) -> None:
    # Find the product and ask it to update its stock with the user's new quantity.
    print("\nUpdate Stock")
    product = inventory.search_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    print(f"Name: {product.name}\nCurrent Stock: {product.stock}")
    new_stock = int(get_valid_input("New Stock Quantity: "))
    product.update_stock(new_stock)
    print("Stock updated successfully!")


def main() -> None:
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
        print("10. Change Order Discount")
        print("11. Load Products from CSV")
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
        elif option == "10":
            change_order_discount(orders)
        elif option == "11":
            import_products(inventory)
        else:
            print("Invalid option. Please choose 1 to 11.")


if __name__ == "__main__":
    main()
