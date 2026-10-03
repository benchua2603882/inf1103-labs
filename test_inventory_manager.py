import contextlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import inventory_manager as manager


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.inventory = [{
            "id": "P001", "name": "Laptop", "price": 1200.0,
            "stock": 15, "transaction_history": [15],
        }]
        self.folder = Path(__file__).with_name(".lab5-test-data")
        self.folder.mkdir(exist_ok=True)
        self.filename = self.folder / "test_inventory.json"
        self.output = io.StringIO()
        self.capture = contextlib.redirect_stdout(self.output)
        self.capture.__enter__()

    def tearDown(self):
        self.capture.__exit__(None, None, None)
        self.filename.unlink(missing_ok=True)

    def test_missing_file_starts_empty(self):
        self.assertEqual(manager.load_inventory(self.folder / "missing.json"), [])

    def test_add_and_reject_duplicate(self):
        with patch("builtins.input", side_effect=["p002", "Mouse", "25.50", "40"]):
            manager.add_product(self.inventory)
        self.assertEqual(self.inventory[-1]["id"], "P002")
        with patch("builtins.input", return_value="p002"):
            manager.add_product(self.inventory)
        self.assertEqual(len(self.inventory), 2)

    def test_stock_replacement_and_history_survive_reload(self):
        with patch("builtins.input", side_effect=["p001", "10"]):
            manager.update_stock(self.inventory)
        self.assertEqual(self.inventory[0]["transaction_history"], [15, -5])
        manager.save_inventory(self.inventory, self.filename)
        self.assertEqual(manager.load_inventory(self.filename), self.inventory)

    def test_search_and_unknown_update(self):
        self.assertIs(manager.search_product(self.inventory, " p001 "), self.inventory[0])
        self.assertIsNone(manager.search_product(self.inventory, "P999"))
        with patch("builtins.input", return_value="P999"):
            manager.update_stock(self.inventory)
        self.assertEqual(self.inventory[0]["stock"], 15)

    def test_invalid_numbers_are_retried(self):
        with patch("builtins.input", side_effect=["-1", "2.5", "abc", "", "0"]):
            self.assertEqual(manager.get_valid_input("Stock: "), 0)
        with patch("builtins.input", side_effect=["nan", "inf", "-2", "abc", "25.50"]):
            self.assertEqual(manager.get_valid_input("Price: ", False), 25.50)

    def test_damaged_file_is_not_overwritten(self):
        for saved in ("{broken", '{"wrong": []}', '[{"id": "P001"}]'):
            self.filename.write_text(saved, encoding="utf-8")
            with self.assertRaises(ValueError):
                manager.load_inventory(self.filename)
            self.assertEqual(self.filename.read_text(encoding="utf-8"), saved)

    def test_menu_saves_then_reloads_on_next_run(self):
        load = manager.load_inventory
        save = manager.save_inventory
        with patch.object(manager, "load_inventory", side_effect=lambda: load(self.filename)), \
                patch.object(manager, "save_inventory", side_effect=lambda data: save(data, self.filename)):
            with patch("builtins.input", side_effect=[
                "bad", "1", "2", "P004", "Monitor", "299.99", "10",
                "3", "P004", "12", "4", "P004", "4", "P999", "5", "6",
            ]):
                manager.main()
            with patch("builtins.input", side_effect=["1", "6"]):
                manager.main()
        saved = json.loads(self.filename.read_text(encoding="utf-8"))
        self.assertEqual(saved[0]["stock"], 12)
        self.assertEqual(saved[0]["transaction_history"], [10, 2])
        self.assertIn("Inventory loaded successfully.", self.output.getvalue())

    def test_save_failure_keeps_menu_open(self):
        with patch.object(manager, "load_inventory", return_value=self.inventory), \
                patch.object(manager, "save_inventory", side_effect=[OSError("denied"), None]) as save, \
                patch("builtins.input", side_effect=["6", "6"]):
            manager.main()
        self.assertEqual(save.call_count, 2)


if __name__ == "__main__":
    unittest.main()
