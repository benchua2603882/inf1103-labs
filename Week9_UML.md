# Week 9 / Lab 7 class diagram

```mermaid
classDiagram
    class Product {
        <<abstract>>
        -str __product_id
        -str __name
        -float __price
        -int __stock
        -list~int~ __transaction_history
        +__init__(product_id, name, price, stock, transaction_history=None)
        +product_id str
        +name str
        +price float
        +stock int
        +transaction_history list~int~
        #_validate_stock(quantity) None
        +update_stock(quantity) None
        +display_information() None
        +get_fulfilment_info()* str
    }
    class PhysicalProduct {
        -float __weight
        +__init__(product_id, name, price, stock, weight, transaction_history=None)
        +weight float
        +display_information() None
        +get_fulfilment_info() str
        +calculate_shipping_cost() float
    }
    class DigitalProduct {
        -float __download_size
        +__init__(product_id, name, price, stock, download_size, transaction_history=None)
        +download_size float
        +display_information() None
        +get_fulfilment_info() str
    }
    class CanBeShipped {
        <<interface>>
        +calculate_shipping_cost()* float
    }
    class Inventory {
        -list~Product~ __products
        +__init__()
        +add_product(product) None
        +search_product(product_id) Product or None
        +get_products() list~Product~
        +display_all() None
    }
    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct
    Inventory "0..*" o-- "0..*" Product : stores
```

- Product is abstract. `get_fulfilment_info()` is abstract, while the shared
  constructor, stock updates and display method have implementations.
- Solid lines with hollow triangles are inheritance. Dashed lines with hollow
  triangles are interface realisation. `CanBeShipped` is implemented as an ABC
  with only an abstract method and no product state or shipping implementation.
- Python spells interface implementation as `PhysicalProduct(Product,
  CanBeShipped)`. This uses one product implementation base and one interface
  contract; it does not inherit implementations from two product classes.
- Product properties and the two measurement properties are read-only. History
  and collection accessors return copies of their lists. `_validate_stock` is static.
- The hollow diamond represents aggregation: Inventory stores Product objects.
  Objects can exist independently and can be shared between inventories.
- Menu and storage remain function-based modules. They are not extra classes.
- The separate SVG is a readable overview; this diagram lists the complete
  application class interfaces. Inherited members are not repeated in subclasses.
