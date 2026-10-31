import math

from product import Product


class DigitalProduct(Product):
    """A downloadable product with its size measured in megabytes."""

    def __init__(self, product_id, name, price, stock, download_size, transaction_history=None):
        super().__init__(product_id, name, price, stock, transaction_history)
        if (
            type(download_size) not in (int, float)
            or not math.isfinite(download_size)
            or download_size < 0
        ):
            raise ValueError("Download size must be a finite, non-negative number.")
        self.__download_size = float(download_size)

    @property
    def download_size(self):
        return self.__download_size

    def display_information(self):
        # Reuse the common product display and add only digital details.
        super().display_information()
        print(f"Download size: {self.__download_size:g} MB")
