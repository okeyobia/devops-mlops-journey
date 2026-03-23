# STAGE 1: Build the application
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtualenv
RUN uv sync --frozen --no-dev

# STAGE 2: Runtime
FROM python:3.12-slim
WORKDIR /app

# Copy the virtualenv from the builder stage
COPY --from=builder /app/.venv /app/.venv
COPY ./app ./app

# Ensure we use the virtualenv's Python and pip
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]