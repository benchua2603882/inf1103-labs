# Week 10 design and predictions

## Planned relationships

- Supplier is created separately and passed to Product. Each Product has one
  Supplier; one Supplier may supply several Products. This is association.
- Inventory keeps Product references. Removing a reference does not destroy the
  product. The existing design permits sharing between inventories, so both ends
  of the aggregation may have zero or more objects.
- Order creates its own OrderLine objects. Each line belongs to exactly one Order
  and cannot be transferred through the public API. This is composition.
- OrderLine refers to one Product without owning it. This is association.

## Supplier interface planned before implementation

```mermaid
classDiagram
    class Supplier {
        -String supplier_id
        -String name
        -String contact_email
        +Supplier(supplier_id: String, name: String, contact_email: String)
        +supplier_id String
        +name String
        +contact_email String
        +display_information() void
    }
    Supplier "1" -- "0..*" Product : supplies
```

The public supplier fields in this diagram are read-only properties backed by
private attributes. The final diagram will include all application classes.

## Predictions recorded before running relationship checks

### Section 2 supplier variable

Deleting the local `supplier` variable should not stop the products from showing
the supplier information. Each product still holds a reference to the same
Supplier object. `del` removes the variable binding, not every reference to the
object.

### Section 3 inventory removal

The product should still work after removal from Inventory A, because the test
code still refers to it. Inventory only removes its own reference. The same
object can then be added to Inventory B.

### Section 4 shared product in two orders

Adding one existing Product once to each of two Orders should create two separate
OrderLine objects referring to one shared Product object. Other products and
lines added in the wider test are separate from these counts.

### Section 7 fulfilment output

The physical product should return `This product requires physical shipping.`
The digital product should return `This product is delivered digitally by download.`
The same loop can call the method on both products because each subclass supplies
its own implementation.

## Results still to be checked

The four relationship checks have not been run yet. Their actual results and any
differences will be recorded in the final Word notes after implementation.
The optional Section 10 reflection will not be included.
