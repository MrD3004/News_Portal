# Dockerfile
FROM python:3.13-slim

# Prevent Python from buffering stdout/stderr and writing pyc
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies (build tools + MySQL dev libs + MariaDB client + netcat)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    mariadb-client \
    netcat-openbsd \
    pkg-config \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Upgrade pip tooling
RUN pip install --upgrade pip setuptools wheel

# Copy dependency manifests first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt

# Install project dependencies (no cache to reduce image size)
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy project source
COPY . /app

# Ensure entrypoint and wait-for-db scripts are executable
RUN chmod 755 /app/docker/entrypoint.sh /app/docker/wait-for-db.sh

# Create non-root system user and set ownership
RUN useradd --system --create-home --shell /bin/bash django \
    && mkdir -p /app/staticfiles /app/media \
    && chown -R django:django /app

USER django

# Expose Django port
EXPOSE 8000

# Default entrypoint delegates to script (handles migrations, collectstatic, server)
ENTRYPOINT ["/app/docker/entrypoint.sh"]






