import math


class Product:
    """Represent one product and control changes to its stock."""

    def __init__(self, product_id, name, price, stock, transaction_history=None):
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if type(price) not in (int, float) or not math.isfinite(price) or price < 0:
            raise ValueError("Price must be a finite, non-negative number.")
        self._validate_stock(stock)

        # Keep the Week 5 quantity history when restoring an existing product.
        if transaction_history is None:
            transaction_history = [stock]
        if not isinstance(transaction_history, list) or any(
            type(change) is not int for change in transaction_history
        ):
            raise ValueError("Transaction history must contain whole-number changes.")
        if sum(transaction_history) != stock:
            raise ValueError("Transaction history must match current stock.")

        self.__product_id = product_id.strip().upper()
        self.__name = name.strip()
        self.__price = float(price)
        self.__stock = stock
        self.__transaction_history = transaction_history.copy()

    @staticmethod
    def _validate_stock(quantity):
        if type(quantity) is not int or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")

    # Read-only properties let other code read values without changing them.
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    @property
    def transaction_history(self):
        # Return a copy so callers cannot change the product's internal history.
        return self.__transaction_history.copy()

    def update_stock(self, quantity):
        """Replace the stock total and record the quantity change."""
        self._validate_stock(quantity)
        self.__transaction_history.append(quantity - self.__stock)
        self.__stock = quantity

    def display_information(self):
        print(
            f"ID: {self.__product_id} | Name: {self.__name} | "
            f"Price: ${self.__price:.2f} | Stock: {self.__stock}"
        )
