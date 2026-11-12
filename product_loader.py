import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    # Opening the file can fail before we get any rows to read.
    try:
        file = open(path, newline="", encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    except OSError as error:
        print(f"Unable to open products file: {error}")
    else:
        loaded = 0
        try:
            with file:
                rows = csv.reader(file, strict=True)
                header = next(rows, None)
                expected = ["product_type", "product_id", "name", "price", "stock_quantity"]
                if header != expected:
                    print("Products file has a missing or incorrect header.")
                    return
                for row_number, row in enumerate(rows, start=2):
                    # A bad row should not stop the remaining products loading.
                    try:
                        if len(row) != 5:
                            raise ValueError("Expected five values in the row.")
                        product_type, product_id, name, price, stock = row
                        product = ProductFactory.create(
                            product_type.strip(), product_id, name,
                            float(price), int(stock), supplier,
                        )
                        inventory.add_product(product)
                        loaded += 1
                    except ValueError as error:
                        print(f"Skipping row {row_number}: {error}")
        except (OSError, UnicodeError, csv.Error) as error:
            # Stop reading if the file itself is damaged or cannot be read.
            print(f"Unable to read products file: {error}")
        print(f"{loaded} products loaded.")
    finally:
        # This runs whether loading worked or an expected error occurred.
        print("Load attempt finished.")
