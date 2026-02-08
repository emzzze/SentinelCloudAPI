#!/bin/bash
set -e

echo "=== Sentinel Cloud API Deployment ==="

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found"
    echo "Copy .env.example to .env and configure"
    exit 1
fi

# Build
echo "Building Docker image..."
docker compose build

# Stop existing
echo "Stopping existing containers..."
docker compose down

# Start fresh
echo "Starting containers..."
docker compose up -d

# Wait for health check
echo "Waiting for health check..."
sleep 10

# Test
echo "Testing API..."
curl -f http://localhost:8000/ || exit 1

echo "=== Deployment Complete ==="
docker compose ps
