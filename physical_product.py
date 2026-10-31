import math

from product import Product


class PhysicalProduct(Product):
    """A product with a physical weight in kilograms."""

    def __init__(self, product_id, name, price, stock, weight, transaction_history=None):
        super().__init__(product_id, name, price, stock, transaction_history)
        if type(weight) not in (int, float) or not math.isfinite(weight) or weight < 0:
            raise ValueError("Weight must be a finite, non-negative number.")
        self.__weight = float(weight)

    @property
    def weight(self):
        return self.__weight

    def display_information(self):
        # Reuse the common product display and add only physical details.
        super().display_information()
        print(f"Weight: {self.__weight:g} kg")
