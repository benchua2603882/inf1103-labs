from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct


class ProductFactory:
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier, weight: float = 0.0,
               download_size: float = 0.0,
               transaction_history: list[int] | None = None) -> Product:
        # The lab CSV has no weight or size, so its sample products use zero.
        # The menu and JSON loader can pass the actual values instead.
        if product_type == "physical":
            return PhysicalProduct(
                product_id, name, price, stock_quantity, weight, supplier,
                transaction_history,
            )
        elif product_type == "digital":
            return DigitalProduct(
                product_id, name, price, stock_quantity, download_size, supplier,
                transaction_history,
            )
        else:
            # Let the caller decide how to report an unsupported type.
            raise ValueError(f"Unknown product type: {product_type}")
