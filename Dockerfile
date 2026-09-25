FROM python:3.11-slim

WORKDIR /app

COPY persistent_auditor.py .

CMD ["python", "persistent_auditor.py"]

# Build and run the Docker image with the following commands: