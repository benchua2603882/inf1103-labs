import json
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
    print("Inventory loaded successfully.")
    return inventory


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
    inventory = load_inventory()
    display_all(inventory)


if __name__ == "__main__":
    main()
