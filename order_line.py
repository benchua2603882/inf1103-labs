from product import Product


class OrderLine:
    """One product and its quantity inside an order."""

    def __init__(self, product: Product, quantity: int) -> None:
        # The order makes this line, but the product is an existing object.
        if not isinstance(product, Product):
            raise TypeError("An order line needs a Product object.")
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Order quantity must be a positive whole number.")
        self.__product: Product = product
        self.__quantity: int = quantity

    @property
    def product(self) -> Product:
        return self.__product

    @property
    def quantity(self) -> int:
        return self.__quantity

    def calculate_subtotal(self) -> float:
        # Multiply the price of one product by the amount ordered.
        return self.__product.price * self.__quantity

    def display_information(self) -> None:
        print(f"{self.__product.product_id} | {self.__product.name} | "
              f"Quantity: {self.__quantity} | Subtotal: ${self.calculate_subtotal():.2f}")
