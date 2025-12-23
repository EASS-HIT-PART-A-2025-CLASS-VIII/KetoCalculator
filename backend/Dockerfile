# syntax=docker/dockerfile:1

FROM public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 AS lwa

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Install uv (build-time tool)
RUN pip install --no-cache-dir uv

# Lambda Web Adapter extension
COPY --from=lwa /lambda-adapter /opt/extensions/aws-lambda-adapter

# Copy deps + code
COPY pyproject.toml uv.lock* /app/
COPY app /app/app

# Install into a venv in /opt (read-only is fine at runtime)
RUN uv venv /opt/venv && uv sync --no-dev

EXPOSE 8080

# Run uvicorn directly (NO uv at runtime)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
