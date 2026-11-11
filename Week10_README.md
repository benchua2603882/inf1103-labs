# Week 10 Lab 8

Run `python inventory_manager.py` from this folder.

## Source files

Submit all ten application modules together:

- inventory_manager.py
- inventory_storage.py
- inventory.py
- product.py
- physical_product.py
- digital_product.py
- can_be_shipped.py
- supplier.py
- order.py
- order_line.py

The existing menu options 1 to 6 still handle inventory. Option 7 creates an
order, option 8 displays orders, and option 9 removes a line from an order.
Orders last for the current session only and do not deduct or reserve stock.
Order totals use current product prices, as in the labsheet's subtotal formula.

When adding a product, enter a supplier ID. An ID already in the inventory reuses
that Supplier object. Otherwise, enter its name and email. Older saved records
use an explicit Supplier not recorded placeholder until genuine details are
provided. No supplier business details have been invented for your old records.

## Relationship design

Product stores a Supplier reference: association. Inventory stores independent
Product objects: aggregation. Order creates and manages OrderLine objects:
composition. OrderLine refers to Product without owning it: association.

Supplier references are reused when loading products with the same supplier ID.
Conflicting details for one ID are rejected. Inventory can find and remove a
Product without destroying it. Orders accept a Product and quantity, not a line
created by another order. List accessors return copies of the lists.

All application function parameters and returns are annotated, along with class
attributes and object collections. Type hints describe intended types; they do
not automatically enforce them. Direct checks and an annotation-presence audit
were performed, not a full static type-checker run.

## Notes and diagram

`Week10_Predict_First_Notes.docx` contains the four predictions, actual results,
comparisons, required LSP diagnosis and UML review. The optional reflection task
is omitted. Review these drafted answers in your own words before submission.
`Week10_UML.svg` contains the coloured UML class overview and relationship legend.
`Week10_design.md` records the decisions and staged observations.

## Verification completed

Local checks verified all four predictions, input validation, order subtotals,
line removal, independent product lifetime, supplier sharing, JSON round trips,
and both product types through a common Product function. Docker checks repeated
association, aggregation, composition, polymorphism, stock updates, order menu
operations and JSON loading. A fresh container restored both product subclasses
and their shared Supplier object. The example order total was $237.50; removing
the first line left $37.50.

`Week10_example.json` contains demonstration products and a sample supplier using
an example.com address. It was produced by verification, separate from your real
inventory. No new test files were added. Your original inventory is preserved.

## Docker and submission evidence

```powershell
docker build -t inventory-manager:week10 .
docker run --rm -it -v "${PWD}:/app" -w /app inventory-manager:week10
git status
git log --oneline -7
```

The Dockerfile copies all ten modules. The folder mount uses local code and keeps
inventory saves on the host. After building for the updated Dockerfile, Python-only
edits do not require rebuilding while using this mount.

For a demonstration using the separate sample JSON, without changing your main
inventory file, mount it over the container's inventory.json:

```powershell
docker run --rm -it -v "${PWD}:/app" --mount "type=bind,source=$($PWD.Path)\Week10_example.json,target=/app/inventory.json" -w /app inventory-manager:week10
```

Capture current screenshots showing the Git and Docker workflow, product details,
and order creation/display/removal. For relationship and LSP evidence, also show
the object-identity and shared-function checks from your lab demonstration;
ordinary menu screenshots alone do not prove all object relationships.
The old Lab 7 screenshots do not show this lab's new features.

The draft ZIP includes source, data, Word notes, UML, Dockerfile and Git log.
Screenshots still need to be added. Refresh the generated log and ZIP after the
final commit. Pushing and submission require your separate instruction.
