from product import Product


class Inventory:
    """Manage a collection of Product objects."""

    def __init__(self):
        # Start with an empty collection of product objects.
        self.__products = []

    def add_product(self, product):
        # Add a product only if it is valid and its ID is not already in use.
        if not isinstance(product, Product):
            raise TypeError("Inventory can only contain Product objects.")
        if self.search_product(product.product_id) is not None:
            raise ValueError("Product ID already exists.")
        self.__products.append(product)

    def search_product(self, product_id):
        # Find a product by ID, ignoring letter case; return None if it is missing.
        product_id = product_id.strip().upper()
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def get_products(self):
        # Return a list copy so callers cannot add or remove stored products directly.
        return self.__products.copy()

    def display_all(self):
        # Let each product display its own details, including its type-specific fields.
        print("\nCurrent Inventory")
        print("-" * 60)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 60)
