from product import Product
from order_line import OrderLine


class Order:
    """Create and manage the lines belonging to one order."""

    def __init__(self, order_id: str) -> None:
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("Order ID cannot be empty.")
        self.__order_id: str = order_id.strip().upper()
        self.__order_lines: list[OrderLine] = []

    @property
    def order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Always make a new line here instead of accepting another order's line.
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def get_order_lines(self) -> list[OrderLine]:
        # Return a copy so changing the list cannot change the order's lines.
        return self.__order_lines.copy()

    def remove_order_line(self, line_number: int) -> None:
        # The displayed line numbers start at 1.
        if type(line_number) is not int or not 1 <= line_number <= len(self.__order_lines):
            raise ValueError("Order line number was not found.")
        self.__order_lines.pop(line_number - 1)

    def calculate_total(self) -> float:
        # Ask each line for its subtotal and add them together.
        total = 0.0
        for line in self.__order_lines:
            total += line.calculate_subtotal()
        return total

    def display_information(self) -> None:
        print(f"\nOrder: {self.__order_id}")
        if not self.__order_lines:
            print("No order lines.")
        for number, line in enumerate(self.__order_lines, start=1):
            print(f"Line {number}: ", end="")
            line.display_information()
        print(f"Order total: ${self.calculate_total():.2f}")
