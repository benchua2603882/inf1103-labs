import json
from pathlib import Path

from inventory import Inventory
from product import Product


INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory(filename=INVENTORY_FILE):
    inventory = Inventory()
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("inventory.json not found. Starting with an empty inventory.")
        return inventory

    # Dictionaries are only used at the JSON boundary, not as live products.
    if not isinstance(data, list):
        raise ValueError("Saved inventory must be a list of products.")
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each saved product must be a JSON object.")
        history = item.get("transaction_history", [item.get("stock")])
        if not isinstance(history, list):
            raise ValueError("Saved transaction history must be a list.")
        product = Product(
            item.get("id"), item.get("name"), item.get("price"),
            item.get("stock"), history,
        )
        inventory.add_product(product)

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, filename=INVENTORY_FILE):
    # Use public properties; private product attributes stay inside Product.
    data = []
    for product in inventory.get_products():
        data.append({
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "transaction_history": product.transaction_history,
        })
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, allow_nan=False)
        file.write("\n")
