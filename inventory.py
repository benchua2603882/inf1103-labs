from product import Product


class Inventory:
    """Manage a collection of Product objects."""

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Inventory can only contain Product objects.")
        if self.search_product(product.product_id) is not None:
            raise ValueError("Product ID already exists.")
        self.__products.append(product)

    def search_product(self, product_id):
        product_id = product_id.strip().upper()
        for product in self.__products:
            if product.product_id == product_id:
                return product
        return None

    def get_products(self):
        # Callers can read the collection, but additions go through add_product().
        return self.__products.copy()

    def display_all(self):
        print("\nCurrent Inventory")
        print("-" * 60)
        if not self.__products:
            print("No products in inventory.")
        for product in self.__products:
            product.display_information()
        print("-" * 60)
