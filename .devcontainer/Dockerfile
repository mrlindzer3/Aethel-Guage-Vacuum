FROM python:3.11-slim

# Install minimal system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY . /workspace
RUN pip install --upgrade pip && pip install -r requirements-dev.txt

CMD ["/bin/bash"]
