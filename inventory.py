from product import Product


class Inventory:
    """Manage a collection of Product objects."""

    def __init__(self) -> None:
        # Start with an empty collection of product objects.
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> None:
        # Add a product only if it is valid and its ID is not already in use.
        if not isinstance(product, Product):
            raise TypeError("Inventory can only contain Product objects.")
        if self.search_product(product.product_id) is not None:
            raise ValueError("Product ID already exists.")
        self.__products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        # Find a product by ID, ignoring letter case; return None if it is missing.
        product_id = product_id.strip().upper()
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        # Keep the old method name working for the existing menu.
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> Product | None:
        # Remove our reference, then return the product so it can be used elsewhere.
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def get_products(self) -> list[Product]:
        # Return a list copy so callers cannot add or remove stored products directly.
        return self.__products.copy()

    def display_all(self) -> None:
        # Let each product display its own details, including its type-specific fields.
        print("\nCurrent Inventory")
        print("-" * 60)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 60)
