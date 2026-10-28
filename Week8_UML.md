# OOP inventory class diagram

The application has two classes. Menu and JSON storage are functions, not classes.
`+` means public, `-` means private, and `#` means an internal helper by convention.
The hollow diamond shows aggregation: Inventory holds Product objects that can
also exist independently. An inventory may contain zero or more products.

```mermaid
classDiagram
    class Product {
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
    }
    class Inventory {
        -list~Product~ __products
        +__init__()
        +add_product(product) None
        +search_product(product_id) Product or None
        +get_products() list~Product~
        +display_all() None
    }
    Inventory "0..*" o-- "0..*" Product : stores
```

The public Product attributes shown above are **read-only properties** backed by
private attributes. `transaction_history` and `Inventory.get_products()` return
list copies. `_validate_stock()` is a static helper. Stock updates must go through
`update_stock()` so validation and history stay together.

## Responsibilities

| Component | Responsibility |
| --- | --- |
| `Product` | Hold one product's information, validate and update its stock, display its information. |
| `Inventory` | Store, add, search and display Product objects. |
| `inventory_manager.py` | Show the menu, collect input and call public methods. |
| `inventory_storage.py` | Convert between JSON records and objects; read and write the file. |

JSON dictionaries are used only for storage. The running inventory holds Product
objects. Neither class asks for input or accesses files.
