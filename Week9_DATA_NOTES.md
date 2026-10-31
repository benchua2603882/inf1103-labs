# Week 9 inventory data

The existing four products in `inventory.json` were converted to physical
products. Their IDs, names, prices, stock quantities and transaction histories
were preserved.

These are **user-approved sample weights for the lab**, not measured weights:

| ID | Product | Sample weight (kg) |
| --- | --- | --- |
| 001 | Laptop NEW | 1.5 |
| HEADPHONE | headphone 2.0 | 0.3 |
| 003 | desktop 1000 | 8 |
| 004 | laptop 2040 | 2 |

`inventory_example.json` is separate demonstration data with one physical
product and one digital product. Its names, prices, stock, weight and download
size are sample values. It is not loaded instead of your inventory automatically.

Saved products now require `type` (`physical` or `digital`) and the corresponding
`weight` in kilograms or `download_size` in megabytes. Loading recreates the
appropriate subclass. Unknown types and missing measurements are rejected
without overwriting the saved file.

When adding a product, choose its type before entering its details. Shipping
costs for physical products use the lab rule of $5 per kilogram per unit.
Digital products have no shipping cost calculation.
