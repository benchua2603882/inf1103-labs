FROM python:3.11-slim

WORKDIR /app

COPY auditor.py .

CMD ["python", "auditor.py"]

# Build and run the Docker image with the following commands: