# Minimal Dockerfile for reproducible environment
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip && pip install -r requirements-dev.txt
CMD ["python3", "-c", "print(\"Aethel lab container ready\")"]
