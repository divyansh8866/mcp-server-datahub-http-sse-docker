# Dockerfile
FROM python:3.11-slim

# System deps (uv needs curl; some libs need build-essential)
RUN apt-get update && apt-get install -y curl build-essential && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager/runner)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

# App
WORKDIR /app
COPY . /app

# Install deps as declared by pyproject.toml / uv.lock
RUN uv sync --frozen --no-dev

# Runtime env (override at docker run)
ENV DATAHUB_GMS_URL=""
ENV DATAHUB_GMS_TOKEN=""

# Expose HTTP (default) and optional SSE port
EXPOSE 8000

# Default: HTTP (stateless) for max compatibility/simplicity
ENTRYPOINT ["uv", "run", "mcp-server-datahub", "--transport", "http"]