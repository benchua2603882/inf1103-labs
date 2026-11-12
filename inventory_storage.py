import json
from pathlib import Path

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from supplier import Supplier
from product_factory import ProductFactory


INVENTORY_FILE = Path(__file__).with_name("inventory.json")


def load_inventory(filename: str | Path = INVENTORY_FILE) -> Inventory:
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
    suppliers: dict[str, Supplier] = {}
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("Each saved product must be a JSON object.")
        # Older records have no supplier details, so label them as not recorded.
        supplier_data = item.get("supplier", {
            "id": "UNASSIGNED", "name": "Supplier not recorded", "contact_email": "Not provided",
        })
        if not isinstance(supplier_data, dict):
            raise ValueError("Saved supplier details must be a JSON object.")
        supplier = Supplier(supplier_data.get("id"), supplier_data.get("name"),
                            supplier_data.get("contact_email"))
        if supplier.supplier_id in suppliers:
            existing = suppliers[supplier.supplier_id]
            if existing.name != supplier.name or existing.contact_email != supplier.contact_email:
                raise ValueError("The same supplier ID has conflicting details.")
            supplier = existing
        else:
            suppliers[supplier.supplier_id] = supplier
        history = item.get("transaction_history", [item.get("stock")])
        if not isinstance(history, list):
            raise ValueError("Saved transaction history must be a list.")
        product_type = item.get("type")
        # The factory chooses the class; this function only reads saved data.
        product = ProductFactory.create(
            product_type, item.get("id"), item.get("name"), item.get("price"),
            item.get("stock"), supplier, weight=item.get("weight"),
            download_size=item.get("download_size"), transaction_history=history,
        )
        inventory.add_product(product)

    print("inventory.json found.")
    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory: Inventory, filename: str | Path = INVENTORY_FILE) -> None:
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
            "supplier": {
                "id": product.supplier.supplier_id,
                "name": product.supplier.name,
                "contact_email": product.supplier.contact_email,
            },
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
