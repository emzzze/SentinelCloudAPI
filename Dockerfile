# ===========================================================================
# SENTINEL CLOUD API - PRODUCTION HARDENED DOCKERFILE
# Multi-stage build with non-root user and minimal attack surface
# ===========================================================================

# --- Stage 1: Build Stage ---
FROM python:3.11-slim AS builder

WORKDIR /build

# Prevent Python from writing .pyc files and enable output buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Runtime Stage ---
FROM python:3.11-slim

# Security: Create non-root user (Principle of Least Privilege)
RUN groupadd -r sentineluser && useradd -r -g sentineluser sentineluser

WORKDIR /app

# Copy only the installed dependencies from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=sentineluser:sentineluser . .

# Security: Remove unnecessary packages and clean up
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Security: Set file permissions
RUN chmod -R 755 /app && \
    chmod 644 /app/*.py

# Switch to non-root user
USER sentineluser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Expose port
EXPOSE 8000

# Start application with production-ready settings
CMD ["uvicorn", "sentinel_api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
