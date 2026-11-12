FROM python:3.11-slim

WORKDIR /app

COPY inventory_manager.py inventory_storage.py inventory.py product.py ./
COPY physical_product.py digital_product.py can_be_shipped.py ./
COPY supplier.py order.py order_line.py ./
COPY discount_strategy.py ./
COPY product_factory.py ./
COPY product_loader.py products.csv ./

CMD ["python", "inventory_manager.py"]

# Mount the project folder at /app to use local code and persist inventory.json.
