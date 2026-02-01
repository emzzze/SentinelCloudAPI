#!/bin/bash

echo "=== SENTINEL CLOUD API AUTHENTICATION TEST ==="
echo ""

# Try to register (will fail if user exists, that's ok)
echo "1. Attempting registration..."
REGISTER=$(curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"SentinelAdmin2026!","role":"superuser"}')
echo "$REGISTER"
echo ""

# Login (works whether user is new or existing)
echo "2. Logging in..."
LOGIN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"SentinelAdmin2026!"}')
echo "$LOGIN"
echo ""

# Extract token
TOKEN=$(echo "$LOGIN" | grep -o '"access_token":"[^"]*' | sed 's/"access_token":"//')
echo "Extracted Token: $TOKEN"
echo ""

# Test protected vault/encrypt
echo "3. Testing protected vault/encrypt..."
ENCRYPT_RESULT=$(curl -s -X POST http://localhost:8000/vault/encrypt \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"secret":"MySecretAPIKey_2026"}')
echo "$ENCRYPT_RESULT"
echo ""

# Test auth/me
echo "4. Testing /auth/me..."
ME_RESULT=$(curl -s -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN")
echo "$ME_RESULT"
echo ""

echo "=== TEST COMPLETE ==="
