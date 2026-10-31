# Week 9 / Lab 7: Inheritance, overriding and abstraction

## Run the application

Keep these seven modules together and run `python inventory_manager.py`:

| Module | Purpose |
| --- | --- |
| `product.py` | Abstract Product with shared validation, stock history and display. |
| `physical_product.py` | PhysicalProduct adds weight, fulfilment and shipping cost. |
| `digital_product.py` | DigitalProduct adds download size and digital fulfilment. |
| `can_be_shipped.py` | Interface-style ABC requiring shipping-cost calculation. |
| `inventory.py` | Manages a collection of Product objects. |
| `inventory_manager.py` | Menu and user input. |
| `inventory_storage.py` | Converts objects to/from JSON and performs file operations. |

Choose Add Product, then select physical or digital. Enter the common details,
then weight in kg or download size in MB. Display and Search call the object's
overridden display method, including its fulfilment information. Stock updates
replace the quantity and record the difference in its transaction history.
Save and Exit both persist the inventory; Exit stays open if saving fails.

## Class design

Both subclasses call `super().__init__()` and `super().display_information()`.
Product cannot be instantiated because `get_fulfilment_info()` is abstract.
CanBeShipped contains only an abstract contract, with no product state or shipping
algorithm. PhysicalProduct implements it using $5 per kg per unit. DigitalProduct
does not implement shipping. Inventory calls public product methods and does not
calculate shipping or change product internals.

`Week9_UML.svg` provides the diagram overview; `Week9_UML.md` contains the complete
class interfaces. Interface realisation is dashed; inheritance is solid, with
hollow triangles pointing towards the interface or superclass.

## Saved data

The main `inventory.json` preserves your existing products and histories, adding
their physical type and approved sample weights. See `Week9_DATA_NOTES.md`.
`inventory_example.json` provides separate mixed physical/digital sample data.
JSON includes `type` and either `weight` or `download_size`, so loading creates
the correct subclass. Invalid or unconverted records produce a loading error
without being replaced with empty data.

## Docker workflow

With Docker Desktop running, execute these PowerShell commands from this folder:

```powershell
docker build -t inventory-manager:week9 .
docker run --rm -it -v "${PWD}:/app" -w /app inventory-manager:week9
```

The Dockerfile now copies all seven modules. Rebuild once for that Dockerfile
change. Later Python edits are immediately available through the full-folder
mount. Saved JSON remains on the host when the container is removed.

## Git and submission

`.gitignore` excludes Python caches, virtual environments, `.env`, editor settings
and generated Week 9 submission artifacts. Existing personal ignore entries are
preserved. Unrelated local deletions are not part of the Week 9 commits.

Inspect changes before staging. The handout's `git add .` would also stage your
unrelated deletions, so use explicit Week 9 paths until those are resolved.
Review commit history with `git log`; export it with `git log > Week9_log.txt`.

Include the seven modules, JSON files, updated UML and screenshots of the Git and
Docker workflow in your submission. Capture a Docker run showing physical and
digital details and a subsequent run confirming saved data was restored.
The submission ZIP remains a draft until required screenshots are included.
Nothing is uploaded or pushed without your separate instruction.

Useful commands to include in the screenshots:

```powershell
git status
git log --oneline -6
docker images inventory-manager:week9
docker run --rm -it -v "${PWD}:/app" -w /app inventory-manager:week9
```

## Verification completed on 31 October 2026

Direct checks were run without adding test files:

- Product and CanBeShipped reject direct construction; incomplete interface
  implementations also reject construction.
- Both subclasses display common and specialised information and return fulfilment
  descriptions. Physical shipping was checked at 0, 0.5, 1.5 and 8 kg.
- DigitalProduct does not implement CanBeShipped or a shipping-cost method.
- The menu handles both types, all six options, invalid inputs, duplicate IDs,
  unknown IDs, stock histories and save failures.
- JSON round trips preserve type, measurements and histories. Invalid saved
  records are rejected without overwriting the file.
- Your four records retain their original IDs, names, prices, stock and history.
- The seven-module Docker image built successfully as `inventory-manager:week9`.
- A Docker menu run against a separate sample-data copy added digital product
  DEMO-D002 (120.5 MB), updated DEMO-P001 to stock 16, searched, saved and exited.
- A fresh container restored DEMO-P001 as PhysicalProduct with weight 1.5 kg,
  stock 16 and history `[15, 1]`, and DEMO-D002 as DigitalProduct with size
  120.5 MB and stock 10. Your main inventory was not changed by this check.
- All seven application modules imported successfully from the image without a
  bind mount. The UML SVG was rendered and visually checked.

These results describe executed checks; they are not substitutes for the required
screenshots. The draft ZIP's Git log should be refreshed after the final commit.

## Optional extension

SubscriptionProduct is optional and is not included. The base Product and
Inventory can support a new subclass without changes, but the current menu and
storage dispatch explicitly recognise two types. Adding a type requires extending
those dispatch points. A type registry/factory would reduce those changes; this
is separate from inheritance itself.
