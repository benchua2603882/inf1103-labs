import math

from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped


# Product supplies shared implementation; CanBeShipped supplies only a contract.
class PhysicalProduct(Product, CanBeShipped):
    """A product with a physical weight in kilograms."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 weight: float, supplier: Supplier,
                 transaction_history: list[int] | None = None) -> None:
        # Set up the shared product details, then check and store its weight.
        super().__init__(product_id, name, price, stock, supplier, transaction_history)
        if type(weight) not in (int, float) or not math.isfinite(weight) or weight < 0:
            raise ValueError("Weight must be a finite, non-negative number.")
        self.__weight: float = float(weight)

    @property
    def weight(self) -> float:
        # Read the weight in kilograms.
        return self.__weight

    def get_fulfilment_info(self) -> str:
        # Describe how a physical product reaches the customer.
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        # Simple lab rule: $5 per kilogram for one product unit.
        return round(self.__weight * 5.0, 2)

    def display_information(self) -> None:
        # Reuse the common product display and add only physical details.
        super().display_information()
        print(f"Weight: {self.__weight:g} kg")
        print(self.get_fulfilment_info())
        print(f"Shipping cost: ${self.calculate_shipping_cost():.2f}")
