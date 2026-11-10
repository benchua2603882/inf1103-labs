import math

from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    """A downloadable product with its size measured in megabytes."""

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 download_size: float, supplier: Supplier,
                 transaction_history: list[int] | None = None) -> None:
        # Set up the shared product details, then check and store its download size.
        super().__init__(product_id, name, price, stock, supplier, transaction_history)
        if (
            type(download_size) not in (int, float)
            or not math.isfinite(download_size)
            or download_size < 0
        ):
            raise ValueError("Download size must be a finite, non-negative number.")
        self.__download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        # Read the download size in megabytes.
        return self.__download_size

    def get_fulfilment_info(self) -> str:
        # Describe how a digital product reaches the customer.
        return "This product is delivered digitally by download."

    def display_information(self) -> None:
        # Reuse the common product display and add only digital details.
        super().display_information()
        print(f"Download size: {self.__download_size:g} MB")
        print(self.get_fulfilment_info())
