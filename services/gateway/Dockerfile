# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copy requirements (Gateway + Shared)
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy Application Code
COPY shared /app/shared
COPY services/gateway /app/services/gateway

# Environment Variables
ENV PYTHONPATH=/app
ENV MODULE_NAME="services.gateway.src.main"
ENV VARIABLE_NAME="app"
ENV PORT=8000

# Expose Port
EXPOSE 8000

# Run Command
CMD ["uvicorn", "services.gateway.src.main:app", "--host", "0.0.0.0", "--port", "8000"]
