import json
from pathlib import Path

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory(filename=INVENTORY_FILE):
    # Read JSON and rebuild the correct product objects; start empty if no file exists.
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
        product_type = item.get("type")
        if product_type == "physical":
            product = PhysicalProduct(
                item.get("id"), item.get("name"), item.get("price"),
                item.get("stock"), item.get("weight"), history,
            )
        elif product_type == "digital":
            product = DigitalProduct(
                item.get("id"), item.get("name"), item.get("price"),
                item.get("stock"), item.get("download_size"), history,
            )
        else:
            raise ValueError(
                f"Product {item.get('id', '(unknown)')} needs type 'physical' or 'digital' "
                "and its weight or download size."
            )
        inventory.add_product(product)

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, filename=INVENTORY_FILE):
    # Save each product's type and details so loading can restore the same kind of object.
    # Use public properties; private product attributes stay inside Product.
    data = []
    for product in inventory.get_products():
        item = {
            "id": product.product_id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "transaction_history": product.transaction_history,
        }
        if isinstance(product, PhysicalProduct):
            item["type"] = "physical"
            item["weight"] = product.weight
        elif isinstance(product, DigitalProduct):
            item["type"] = "digital"
            item["download_size"] = product.download_size
        else:
            raise ValueError("Cannot save an unsupported product type.")
        data.append(item)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, allow_nan=False)
        file.write("\n")
