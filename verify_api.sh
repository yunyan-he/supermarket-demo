#!/bin/bash

echo "Starting Server..."
# We assume the server is running on port 8000. If not, we might need to start it.
# For this script, we'll assume the user or a background process has started it.
# But to be safe in this agentic context, I'll rely on the agent starting it separately or checking it.
# Actually, I'll just make requests assuming it's up.

BASE_URL="http://127.0.0.1:8000"

echo "1. Testing GET /api/products"
curl -s "$BASE_URL/api/products" | head -c 200
echo "..."
echo ""

echo "2. Testing GET /api/product/1001 (Milk)"
curl -s "$BASE_URL/api/product/1001"
echo ""

echo "3. Testing POST /api/checkout (Valid)"
curl -s -X POST "$BASE_URL/api/checkout" \
     -H "Content-Type: application/json" \
     -d '{
           "participant_external_id": "P-101",
           "items": [
             {"barcode": "1001", "quantity": 1},
             {"barcode": "1002", "quantity": 2}
           ]
         }'
echo ""

echo "4. Testing POST /api/checkout (Invalid - Insufficient Stock)"
# Milk stock is 50. Let's try to buy 1000.
curl -s -X POST "$BASE_URL/api/checkout" \
     -H "Content-Type: application/json" \
     -d '{
           "participant_external_id": "P-101",
           "items": [
             {"barcode": "1001", "quantity": 1000}
           ]
         }'
echo ""

echo "5. Testing POST /api/external/camera"
curl -s -X POST "$BASE_URL/api/external/camera" \
     -H "Content-Type: application/json" \
     -d '{"event": "staring", "timestamp": "2023-10-27T10:00:00"}'
echo ""
