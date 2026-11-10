import math
from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    """Represent one product and control changes to its stock."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, transaction_history: list[int] | None = None) -> None:
        # Check the product details before storing them in private attributes.
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if type(price) not in (int, float) or not math.isfinite(price) or price < 0:
            raise ValueError("Price must be a finite, non-negative number.")
        self._validate_stock(stock)
        if not isinstance(supplier, Supplier):
            raise TypeError("Supplier must be a Supplier object.")
        # Keep the same supplier object instead of making a copy.
        self.__supplier: Supplier = supplier

        # Keep the Week 5 quantity history when restoring an existing product.
        if transaction_history is None:
            transaction_history = [stock]
        if not isinstance(transaction_history, list) or any(
            type(change) is not int for change in transaction_history
        ):
            raise ValueError("Transaction history must contain whole-number changes.")
        if sum(transaction_history) != stock:
            raise ValueError("Transaction history must match current stock.")

        self.__product_id: str = product_id.strip().upper()
        self.__name: str = name.strip()
        self.__price: float = float(price)
        self.__stock: int = stock
        self.__transaction_history: list[int] = transaction_history.copy()

    @staticmethod
    def _validate_stock(quantity: int) -> None:
        # Reject negative quantities and values that are not whole numbers.
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")

    @property
    def supplier(self) -> Supplier:
        # The supplier exists separately from this product.
        return self.__supplier

    # Read-only properties let other code read values without changing them.
    @property
    def product_id(self) -> str:
        # Read the product's ID without allowing it to be reassigned.
        return self.__product_id

    @property
    def name(self) -> str:
        # Read the product's name.
        return self.__name

    @property
    def price(self) -> float:
        # Read the price of one unit.
        return self.__price

    @property
    def stock(self) -> int:
        # Read the current quantity; use update_stock() to change it.
        return self.__stock

    @property
    def transaction_history(self) -> list[int]:
        # Return a copy so callers cannot change the product's internal history.
        return self.__transaction_history.copy()

    def update_stock(self, quantity: int) -> None:
        """Replace the stock total and record the quantity change."""
        self._validate_stock(quantity)
        self.__transaction_history.append(quantity - self.__stock)
        self.__stock = quantity

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Subclasses must describe how the product reaches the customer."""
        pass

    def display_information(self) -> None:
        # Print the common details shared by all product types.
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )
        self.__supplier.display_information()
