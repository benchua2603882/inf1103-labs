# Week 8 / Lab 6: OOP inventory management

## Run locally

```powershell
python inventory_manager.py
python -B -m unittest -v test_product test_inventory test_inventory_manager
```

The six menu choices are Display, Add, Update, Search, Save and Exit. Exit saves
before closing. Invalid input is retried or reported. Duplicate product IDs are
rejected without changing the inventory. IDs are case-insensitive.

## Files and design

- `product.py`: Product has private fields and read-only properties. Only
  `update_stock()` changes stock and records its quantity difference.
- `inventory.py`: Inventory holds Product objects, checks duplicate IDs, searches
  and displays the collection. It returns a copy of its product list.
- `inventory_manager.py`: menu and input handling.
- `inventory_storage.py`: loads JSON into Product objects and saves public values
  back to the same JSON structure. File handling is separate from both classes.
- `inventory.json`: current saved products, including their transaction histories.
- `Week8_UML.md` and `Week8_UML.svg`: class diagram and design explanation.

The existing Week 5 JSON remains compatible. A missing file starts an empty
Inventory. Malformed or invalid saved data stops startup without overwriting it.
Tests write to separate files, not to the real inventory.

## Docker: mount the whole project folder

From this folder in PowerShell, with Docker Desktop running:

```powershell
docker build -t inventory-manager:week8 .
docker run --rm -it -v "${PWD}:/app" -w /app inventory-manager:week8
```

The Dockerfile was updated once to include all four application modules. Future
Python-only edits do not require rebuilding when using the whole-folder mount.
The mount also keeps `inventory.json` on the host after the container is removed.
This image name is the local lab image; the PDF's example uses a different tag.

To run the tests in the same environment:

```powershell
docker run --rm -v "${PWD}:/app" -w /app inventory-manager:week8 python -B -m unittest -v test_product test_inventory test_inventory_manager
```

## Evidence and submission

`Week8_evidence` contains actual Docker build, test, menu-run and restart output.
The automated menu run displays products, updates P001 to 16, searches for it,
saves and exits. Its inputs are `1, 3, P001, 16, 4, P001, 5, 6`.
A new container uses `1, 6` to confirm persistence. Piped inputs are not echoed.

Before submission, capture the two screenshots requested by the handout:

1. A terminal showing the Docker run command and running inventory program.
2. A terminal showing your entered menu choice/product details and its result.

Text logs are not screenshots, and older Week 5 screenshots do not demonstrate
this OOP version. Save the new screenshots in `Week8_evidence`.

The submission ZIP should contain the four application Python files, tests,
updated JSON, UML diagram, Git log and evidence. The prepared ZIP remains a draft
until the screenshots are added. `Week8_log.txt` and the ZIP are generated local
submission artifacts, kept outside the commits. Refresh the log after committing
with `git log > Week8_log.txt`, then refresh the ZIP so it includes that commit.
Push and xSite upload are separate actions requiring your instruction.

## Reflection study notes

1. A class is a blueprint; an object is a particular instance of that class.
2. Product is suitable because each item has its own information and stock behavior.
3. ID, name, price, stock and the existing quantity history belong to Product.
4. Product controls stock changes so every change is validated and recorded.
5. Encapsulation keeps state behind private attributes and a public interface.
6. Product represents and manages one product.
7. Inventory manages the collection of products.
8. These separate responsibilities follow SRP; menu and file operations are separate too.
9. The main program uses public properties and methods to show and update products.
10. The main program does not need private attribute names, the internal collection
    layout, or the details of how Product stores and updates its history.
