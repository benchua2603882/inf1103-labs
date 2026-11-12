import unittest

from discount_strategy import (
    DiscountStrategy, NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount,
)
from order import Order
from product_factory import ProductFactory
from supplier import Supplier


class DiscountTests(unittest.TestCase):
    def setUp(self) -> None:
        # Start each test with a fresh order worth $250.
        supplier = Supplier("S1", "Demo Supplier", "demo@example.com")
        self.product = ProductFactory.create("physical", "P1", "Keyboard", 125, 10, supplier)
        self.order = Order("O1")
        self.order.add_order_line(self.product, 2)

    def test_default_and_empty_order(self) -> None:
        self.assertEqual(self.order.calculate_total(), 250)
        self.assertEqual(Order("EMPTY").calculate_total(), 0)

    def test_switch_strategy_on_same_order(self) -> None:
        self.order.set_discount(BulkDiscount(200, 20))
        self.assertEqual(self.order.calculate_total(), 230)
        self.order.set_discount(PercentageDiscount(10))
        self.assertEqual(self.order.calculate_total(), 225)
        self.order.set_discount(StudentDiscount())
        self.assertEqual(self.order.calculate_total(), 237.5)
        self.order.set_discount(NoDiscount())
        self.assertEqual(self.order.calculate_total(), 250)

    def test_shared_strategy_does_not_link_orders(self) -> None:
        shared = PercentageDiscount(10)
        other = Order("O2", shared)
        other.add_order_line(self.product, 2)
        self.order.set_discount(shared)
        self.order.set_discount(NoDiscount())
        self.assertEqual(other.calculate_total(), 225)
        self.assertEqual(self.order.calculate_total(), 250)

    def test_new_strategy_works_without_order_changes(self) -> None:
        # This test-only strategy proves Order can use a new behaviour.
        class FiveDollarsOff(DiscountStrategy):
            def apply(self, total: float) -> float:
                return max(0.0, total - 5)

        self.order.set_discount(FiveDollarsOff())
        self.assertEqual(self.order.calculate_total(), 245)

    def test_bulk_threshold_and_zero_floor(self) -> None:
        discount = BulkDiscount(200, 20)
        self.assertEqual(discount.apply(199), 199)
        self.assertEqual(discount.apply(200), 180)
        self.assertEqual(BulkDiscount(0, 500).apply(250), 0)

    def test_percentage_limits(self) -> None:
        self.assertEqual(PercentageDiscount(0).apply(250), 250)
        self.assertEqual(PercentageDiscount(100).apply(250), 0)
        for value in (-1, 101, float("nan"), float("inf"), True):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    PercentageDiscount(value)

    def test_invalid_bulk_settings_and_strategy(self) -> None:
        for threshold, amount in [(-1, 20), (200, -1), (float("inf"), 20), (200, float("nan"))]:
            with self.subTest(threshold=threshold, amount=amount):
                with self.assertRaises(ValueError):
                    BulkDiscount(threshold, amount)
        with self.assertRaises(TypeError):
            self.order.set_discount("student")
        self.assertEqual(self.order.calculate_total(), 250)


if __name__ == "__main__":
    unittest.main()
