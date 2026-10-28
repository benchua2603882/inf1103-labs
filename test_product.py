import contextlib
import io
import unittest

from product import Product


class ProductTests(unittest.TestCase):
    def test_constructor_and_display(self):
        product = Product(" p001 ", "Laptop", 1200.0, 15)
        self.assertEqual(product.product_id, "P001")
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.price, 1200.0)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            product.display_information()
        self.assertEqual(
            output.getvalue().strip(),
            "ID: P001 | Name: Laptop | Price: $1200.00 | Stock: 15",
        )

    def test_update_replaces_stock_and_preserves_history(self):
        product = Product("P002", "Mouse", 25.50, 50, [40, 10])
        product.update_stock(30)
        product.update_stock(0)
        self.assertEqual(product.stock, 0)
        self.assertEqual(product.transaction_history, [40, 10, -20, -30])

    def test_invalid_update_leaves_state_unchanged(self):
        product = Product("P001", "Laptop", 1200.0, 15)
        for quantity in (-1, 2.5, "10", True):
            with self.subTest(quantity=quantity):
                with self.assertRaises(ValueError):
                    product.update_stock(quantity)
                self.assertEqual(product.stock, 15)
                self.assertEqual(product.transaction_history, [15])

    def test_encapsulation(self):
        history = [40, 10]
        product = Product("P002", "Mouse", 25.50, 50, history)
        history.append(100)
        product.transaction_history.append(100)
        self.assertEqual(product.transaction_history, [40, 10])
        with self.assertRaises(AttributeError):
            product.stock = -1
        self.assertEqual(product.stock, 50)

    def test_invalid_constructor_data(self):
        for arguments in (
            ("", "Laptop", 1200.0, 15),
            ("P001", " ", 1200.0, 15),
            ("P001", "Laptop", -1, 15),
            ("P001", "Laptop", float("nan"), 15),
            ("P001", "Laptop", float("inf"), 15),
            ("P001", "Laptop", 1200.0, -1),
            ("P001", "Laptop", 1200.0, 15, [10]),
            ("P001", "Laptop", 1200.0, 15, [15.0]),
        ):
            with self.subTest(arguments=arguments):
                with self.assertRaises(ValueError):
                    Product(*arguments)


if __name__ == "__main__":
    unittest.main()
