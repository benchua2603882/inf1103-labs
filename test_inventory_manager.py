import contextlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch
from uuid import uuid4

from inventory import Inventory
import inventory_manager as manager
import inventory_storage as storage
from product import Product


class OOPSystemTests(unittest.TestCase):
    def setUp(self):
        folder = Path(__file__).with_name(".lab5-test-data")
        folder.mkdir(exist_ok=True)
        self.filename = folder / f"oop-{uuid4().hex}.json"
        self.output = io.StringIO()
        self.capture = contextlib.redirect_stdout(self.output)
        self.capture.__enter__()

    def tearDown(self):
        self.capture.__exit__(None, None, None)
        self.filename.unlink(missing_ok=True)

    def test_missing_file_returns_empty_inventory(self):
        inventory = storage.load_inventory(self.filename)
        self.assertIsInstance(inventory, Inventory)
        self.assertEqual(inventory.get_products(), [])

    def test_existing_json_round_trip_preserves_data(self):
        # Read the real data but save only to a separate test file.
        original = json.loads(storage.INVENTORY_FILE.read_text(encoding="utf-8"))
        inventory = storage.load_inventory()
        self.assertTrue(all(isinstance(p, Product) for p in inventory.get_products()))
        storage.save_inventory(inventory, self.filename)
        saved = json.loads(self.filename.read_text(encoding="utf-8"))
        self.assertEqual(saved, original)
        reloaded = storage.load_inventory(self.filename)
        self.assertEqual(len(reloaded.get_products()), len(original))

    def test_invalid_saved_data_is_preserved(self):
        valid = {"id": "P001", "name": "Laptop", "price": 1200, "stock": 15}
        invalid_values = [
            "{broken", "{}", "[12]", "[{}]",
            json.dumps([valid, valid]),
            json.dumps([dict(valid, transaction_history=None)]),
            json.dumps([dict(valid, transaction_history=[10])]),
        ]
        for saved in invalid_values:
            with self.subTest(saved=saved):
                self.filename.write_text(saved, encoding="utf-8")
                with self.assertRaises(ValueError):
                    storage.load_inventory(self.filename)
                self.assertEqual(self.filename.read_text(encoding="utf-8"), saved)

    def test_legacy_product_without_history_loads(self):
        self.filename.write_text(json.dumps([
            {"id": "P001", "name": "Laptop", "price": 1200, "stock": 15},
        ]), encoding="utf-8")
        inventory = storage.load_inventory(self.filename)
        self.assertEqual(inventory.search_product("P001").transaction_history, [15])

    def test_all_menu_options_and_restart(self):
        with patch.object(manager, "load_inventory", side_effect=lambda: storage.load_inventory(self.filename)), \
                patch.object(manager, "save_inventory", side_effect=lambda inventory: storage.save_inventory(inventory, self.filename)):
            with patch("builtins.input", side_effect=[
                "bad", "1", "2", "P004", "Monitor", "299.99", "10",
                "2", "p004", "3", "P004", "12", "4", "P004",
                "4", "P999", "3", "P999", "5", "6",
            ]):
                manager.main()
            with patch("builtins.input", side_effect=["1", "6"]):
                manager.main()
        product = storage.load_inventory(self.filename).search_product("P004")
        self.assertEqual(product.stock, 12)
        self.assertEqual(product.transaction_history, [10, 2])
        for message in ("Invalid option", "Product ID already exists", "Product not found", "Stock: 12"):
            self.assertIn(message, self.output.getvalue())

    def test_invalid_user_numbers_are_retried(self):
        with patch("builtins.input", side_effect=["-1", "1.5", "text", "", "0"]):
            self.assertEqual(manager.get_valid_input("Stock: "), 0)
        with patch("builtins.input", side_effect=["nan", "inf", "-1", "text", "25.50"]):
            self.assertEqual(manager.get_valid_input("Price: ", False), 25.50)

    def test_load_failure_does_not_enter_menu_or_save(self):
        with patch.object(manager, "load_inventory", side_effect=ValueError("Invalid saved data")), \
                patch.object(manager, "save_inventory") as save, \
                patch("builtins.input") as user_input:
            manager.main()
        save.assert_not_called()
        user_input.assert_not_called()

    def test_save_failure_does_not_exit(self):
        with patch.object(manager, "load_inventory", return_value=Inventory()), \
                patch.object(manager, "save_inventory", side_effect=[OSError("denied"), None]) as save, \
                patch("builtins.input", side_effect=["6", "6"]):
            manager.main()
        self.assertEqual(save.call_count, 2)
        self.assertIn("Unable to save inventory", self.output.getvalue())


if __name__ == "__main__":
    unittest.main()
