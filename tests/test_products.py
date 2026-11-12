import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from digital_product import DigitalProduct
from inventory import Inventory
from inventory_storage import load_inventory, save_inventory
from order_line import OrderLine
from physical_product import PhysicalProduct
from product_factory import ProductFactory
from supplier import Supplier


class ProductTests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S1", "Demo Supplier", "demo@example.com")

    def test_factory_builds_both_types(self) -> None:
        physical = ProductFactory.create("physical", "P1", "Keyboard", 100, 10,
                                         self.supplier, weight=1.5)
        digital = ProductFactory.create("digital", "D1", "Ebook", 12.5, 10,
                                        self.supplier, download_size=25)
        self.assertIsInstance(physical, PhysicalProduct)
        self.assertIsInstance(digital, DigitalProduct)
        self.assertEqual(physical.weight, 1.5)
        self.assertEqual(digital.download_size, 25)
        self.assertIs(physical.supplier, digital.supplier)

    def test_unknown_type_has_clear_error(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unknown product type: service"):
            ProductFactory.create("service", "S1", "Installation", 30, 5, self.supplier)

    def test_price_validation_for_both_types(self) -> None:
        for kind in ("physical", "digital"):
            for price in (0, -5, float("nan"), float("inf"), True, "12.50"):
                with self.subTest(kind=kind, price=price):
                    with self.assertRaises(ValueError):
                        ProductFactory.create(kind, "X1", "Invalid", price, 5, self.supplier)

    def test_stock_rules_are_shared_by_both_types(self) -> None:
        for kind in ("physical", "digital"):
            for stock in (-1, 1.5, True):
                with self.subTest(kind=kind, stock=stock):
                    with self.assertRaises(ValueError):
                        ProductFactory.create(kind, "X1", "Invalid", 12.5, stock, self.supplier)
            product = ProductFactory.create(kind, "X1", "Valid", 12.5, 5, self.supplier)
            before = product.transaction_history
            with self.assertRaises(ValueError):
                product.update_stock(-1)
            # A rejected update must not change either the stock or its history.
            self.assertEqual(product.stock, 5)
            self.assertEqual(product.transaction_history, before)
            self.assertIsNone(product.update_stock(0))
            self.assertEqual(product.stock, 0)

    def test_order_line_validates_its_quantity(self) -> None:
        product = ProductFactory.create("physical", "P1", "Keyboard", 100, 10, self.supplier)
        for quantity in (0, -1, 1.5, True):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    OrderLine(product, quantity)
        self.assertEqual(OrderLine(product, 2).calculate_subtotal(), 200)

    def test_json_round_trip_preserves_product_details(self) -> None:
        inventory = Inventory()
        inventory.add_product(ProductFactory.create(
            "physical", "P1", "Keyboard", 100, 12, self.supplier,
            weight=1.5, transaction_history=[10, 2],
        ))
        inventory.add_product(ProductFactory.create(
            "digital", "D1", "Ebook", 12.5, 7, self.supplier,
            download_size=25, transaction_history=[10, -3],
        ))
        # Use a temporary file so the test cannot change the real inventory.
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "inventory.json"
            save_inventory(inventory, path)
            with redirect_stdout(io.StringIO()):
                restored = load_inventory(path)
            physical = restored.find_product("P1")
            digital = restored.find_product("D1")
            self.assertEqual(physical.weight, 1.5)
            self.assertEqual(digital.download_size, 25)
            self.assertEqual(physical.transaction_history, [10, 2])
            self.assertEqual(digital.transaction_history, [10, -3])
            self.assertIs(physical.supplier, digital.supplier)
            second_path = Path(folder) / "restored.json"
            save_inventory(restored, second_path)
            self.assertEqual(json.loads(path.read_text()), json.loads(second_path.read_text()))


if __name__ == "__main__":
    unittest.main()
