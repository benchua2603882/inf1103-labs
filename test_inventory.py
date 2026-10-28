import contextlib
import io
import unittest

from inventory import Inventory
from product import Product


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.inventory = Inventory()
        self.laptop = Product("P001", "Laptop", 1200.0, 15)

    def test_add_and_search_products(self):
        mouse = Product("P002", "Mouse", 25.50, 40)
        self.inventory.add_product(self.laptop)
        self.inventory.add_product(mouse)
        self.assertIs(self.inventory.search_product(" p001 "), self.laptop)
        self.assertIs(self.inventory.search_product("p002"), mouse)
        self.assertIsNone(self.inventory.search_product("P999"))

    def test_duplicate_id_is_rejected(self):
        self.inventory.add_product(self.laptop)
        duplicate = Product("p001", "Another laptop", 900.0, 5)
        with self.assertRaises(ValueError):
            self.inventory.add_product(duplicate)
        self.assertEqual(self.inventory.get_products(), [self.laptop])

    def test_dictionary_is_rejected(self):
        with self.assertRaises(TypeError):
            self.inventory.add_product({"id": "P001", "name": "Laptop"})
        self.assertEqual(self.inventory.get_products(), [])

    def test_collection_cannot_be_changed_through_copy(self):
        self.inventory.add_product(self.laptop)
        products = self.inventory.get_products()
        products.clear()
        self.assertIs(self.inventory.search_product("P001"), self.laptop)

    def test_found_product_controls_its_own_stock(self):
        self.inventory.add_product(self.laptop)
        product = self.inventory.search_product("P001")
        product.update_stock(20)
        self.assertEqual(self.laptop.stock, 20)
        self.assertEqual(self.laptop.transaction_history, [15, 5])

    def test_display_empty_and_populated_inventory(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.inventory.display_all()
        self.assertIn("No products in inventory.", output.getvalue())

        self.inventory.add_product(self.laptop)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.inventory.display_all()
        self.assertIn(
            "ID: P001 | Name: Laptop | Price: $1200.00 | Stock: 15",
            output.getvalue(),
        )
        self.assertNotIn("No products", output.getvalue())


if __name__ == "__main__":
    unittest.main()
