FROM python:3.11-slim

WORKDIR /app

COPY auditor.py .

CMD ["python", "auditor.py"]
<<<<<<< HEAD:DockerFile

# Build and run the Docker image with the following commands:
=======
>>>>>>> e161870c4e952726f9482060a1a108c679433b57:Dockerfile
