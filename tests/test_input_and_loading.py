import io
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from inventory import Inventory
from inventory_manager import get_positive_float, main
from product_loader import load_products
from supplier import Supplier


class InputAndLoadingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.inventory = Inventory()
        self.supplier = Supplier("S1", "Demo Supplier", "demo@example.com")
        self.sample = Path(__file__).resolve().parents[1] / "products.csv"

    def test_price_retries_then_returns_valid_value(self) -> None:
        # Supply keyboard answers automatically instead of typing during tests.
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]) as ask:
            with redirect_stdout(io.StringIO()) as output:
                value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(ask.call_count, 3)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])

    def test_zero_and_non_finite_prices_are_retried(self) -> None:
        with patch("builtins.input", side_effect=["0", "nan", "inf", "0.001"]):
            with redirect_stdout(io.StringIO()) as output:
                value = get_positive_float("Price: ")
        self.assertEqual(value, 0.001)
        self.assertEqual(output.getvalue().count("Please enter"), 3)

    def test_sample_csv_skips_bad_rows_and_keeps_loading(self) -> None:
        with redirect_stdout(io.StringIO()) as output:
            load_products(str(self.sample), self.inventory, self.supplier)
        self.assertEqual(output.getvalue().splitlines(), [
            "Skipping row 4: Unknown product type: service",
            "Skipping row 5: could not convert string to float: 'abc'",
            "3 products loaded.",
            "Load attempt finished.",
        ])
        self.assertEqual([p.product_id for p in self.inventory.get_products()],
                         ["P001", "D001", "P003"])
        for product in self.inventory.get_products():
            self.assertIs(product.supplier, self.supplier)
        self.assertEqual(self.inventory.find_product("P001").weight, 0)
        self.assertEqual(self.inventory.find_product("D001").download_size, 0)

    def test_missing_file_still_runs_finally(self) -> None:
        with patch("product_loader.open", side_effect=FileNotFoundError):
            with redirect_stdout(io.StringIO()) as output:
                load_products("missing_products.csv", self.inventory, self.supplier)
        self.assertEqual(output.getvalue().splitlines(), [
            "Products file not found: missing_products.csv", "Load attempt finished.",
        ])
        self.assertEqual(self.inventory.get_products(), [])

    def test_repeated_import_does_not_add_duplicates(self) -> None:
        with redirect_stdout(io.StringIO()) as output:
            load_products(str(self.sample), self.inventory, self.supplier)
            load_products(str(self.sample), self.inventory, self.supplier)
        self.assertEqual(len(self.inventory.get_products()), 3)
        self.assertIn("0 products loaded.", output.getvalue())

    def test_invalid_fields_do_not_stop_later_rows(self) -> None:
        data = "product_type,product_id,name,price,stock_quantity\n"
        data += "physical,A,Invalid,0,1\nphysical,B,Invalid,12,-1\n"
        data += "physical,C,Invalid,12,1.5\nphysical,short\nphysical,D,Valid,12,1\n"
        with patch("product_loader.open", return_value=io.StringIO(data)):
            with redirect_stdout(io.StringIO()) as output:
                load_products("rows.csv", self.inventory, self.supplier)
        self.assertEqual(output.getvalue().count("Skipping row"), 4)
        self.assertEqual(len(self.inventory.get_products()), 1)
        self.assertEqual(self.inventory.find_product("D").price, 12)

    def test_bad_header_still_runs_finally(self) -> None:
        for data in ("", "wrong,header\n"):
            with self.subTest(data=data):
                with patch("product_loader.open", return_value=io.StringIO(data)):
                    with redirect_stdout(io.StringIO()) as output:
                        load_products("header.csv", self.inventory, self.supplier)
                self.assertIn("missing or incorrect header", output.getvalue())
                self.assertTrue(output.getvalue().endswith("Load attempt finished.\n"))

    def test_permission_error_is_reported(self) -> None:
        with patch("product_loader.open", side_effect=PermissionError("No access")):
            with redirect_stdout(io.StringIO()) as output:
                load_products("blocked.csv", self.inventory, self.supplier)
        self.assertIn("Unable to open products file:", output.getvalue())
        self.assertTrue(output.getvalue().endswith("Load attempt finished.\n"))

    def test_csv_read_error_is_reported(self) -> None:
        data = 'product_type,product_id,name,price,stock_quantity\nphysical,P1,"unfinished'
        with patch("product_loader.open", return_value=io.StringIO(data)):
            with redirect_stdout(io.StringIO()) as output:
                load_products("broken.csv", self.inventory, self.supplier)
        self.assertIn("Unable to read products file:", output.getvalue())
        self.assertTrue(output.getvalue().endswith("0 products loaded.\nLoad attempt finished.\n"))

    def test_menu_import_order_and_discount(self) -> None:
        answers = ["11", str(self.sample), "S1", "Demo", "demo@example.com",
                   "7", "O1", "P001", "10", "done",
                   "10", "O1", "2", "101", "4", "8", "6"]
        # Replace saving so this menu test never writes to inventory.json.
        with patch("inventory_manager.load_inventory", return_value=self.inventory):
            with patch("inventory_manager.save_inventory") as save:
                with patch("builtins.input", side_effect=answers):
                    with redirect_stdout(io.StringIO()) as output:
                        main()
        self.assertIn("3 products loaded.", output.getvalue())
        self.assertIn("Percentage must be between 0 and 100.", output.getvalue())
        self.assertIn("Order total: $237.50", output.getvalue())
        save.assert_called_once_with(self.inventory)


if __name__ == "__main__":
    unittest.main()
