# Week 10 complete class diagram

```mermaid
classDiagram
    class Product {
        <<abstract>>
        -Supplier __supplier
        -str __product_id
        -str __name
        -float __price
        -int __stock
        -list~int~ __transaction_history
        +__init__(product_id: str, name: str, price: float, stock: int, supplier: Supplier, transaction_history: list~int~ | None) None
        #_validate_stock(quantity: int) None
        +supplier Supplier
        +product_id str
        +name str
        +price float
        +stock int
        +transaction_history list~int~
        +update_stock(quantity: int) None
        +get_fulfilment_info()* str
        +display_information() None
    }
    class PhysicalProduct {
        -float __weight
        +__init__(product_id: str, name: str, price: float, stock: int, weight: float, supplier: Supplier, transaction_history: list~int~ | None) None
        +weight float
        +get_fulfilment_info() str
        +calculate_shipping_cost() float
        +display_information() None
    }
    class DigitalProduct {
        -float __download_size
        +__init__(product_id: str, name: str, price: float, stock: int, download_size: float, supplier: Supplier, transaction_history: list~int~ | None) None
        +download_size float
        +get_fulfilment_info() str
        +display_information() None
    }
    class CanBeShipped {
        <<interface>>
        +calculate_shipping_cost()* float
    }
    class Supplier {
        -str __supplier_id
        -str __name
        -str __contact_email
        +__init__(supplier_id: str, name: str, contact_email: str) None
        +supplier_id str
        +name str
        +contact_email str
        +display_information() None
    }
    class Inventory {
        -list~Product~ __products
        +__init__() None
        +add_product(product: Product) None
        +find_product(product_id: str) Product | None
        +search_product(product_id: str) Product | None
        +remove_product(product_id: str) Product | None
        +get_products() list~Product~
        +display_all() None
    }
    class Order {
        -str __order_id
        -list~OrderLine~ __order_lines
        +__init__(order_id: str) None
        +order_id str
        +add_order_line(product: Product, quantity: int) None
        +get_order_lines() list~OrderLine~
        +remove_order_line(line_number: int) None
        +calculate_total() float
        +display_information() None
    }
    class OrderLine {
        -Product __product
        -int __quantity
        +__init__(product: Product, quantity: int) None
        +product Product
        +quantity int
        +calculate_subtotal() float
        +display_information() None
    }
    Product <|-- PhysicalProduct
    Product <|-- DigitalProduct
    CanBeShipped <|.. PhysicalProduct
    Supplier "1" -- "0..*" Product : supplies
    Inventory "0..*" o-- "0..*" Product : stores
    Order "1" *-- "0..*" OrderLine : owns
    OrderLine "0..*" -- "1" Product : refers to
```

Public properties are read-only. Constructors and method signatures match the source.
Product and CanBeShipped are abstract; abstract methods are marked with an asterisk.
Inventory permits products to be shared, so a Product may be in zero or more inventories.
Order creates each line internally and has no method for inserting an existing line.
Supplier and Product references do not imply ownership. Lists returned by accessors are copies.
The SVG is an overview; this diagram provides the complete typed interfaces.
