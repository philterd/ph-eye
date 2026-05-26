#!/bin/bash -e

assert_contains() {
    local response="$1"
    local expected="$2"
    local label="$3"
    if echo "$response" | grep -q "$expected"; then
        echo "PASS: $label"
    else
        echo "FAIL: $label — expected '$expected' in response: $response"
        exit 1
    fi
}

echo "Testing pii_base (port 8001)..."
RESPONSE=$(curl -s -X POST http://localhost:8001/find \
  -H "Content-Type: application/json" \
  -d '{"text": "George Washington was president and he lived in Virginia.", "labels": ["Person", "Place"], "threshold": 0.5}')
echo "$RESPONSE"
assert_contains "$RESPONSE" "George Washington" "pii_base: person detected"
assert_contains "$RESPONSE" "Virginia" "pii_base: place detected"
echo

echo "Testing hospitals (port 8002)..."
RESPONSE=$(curl -s -X POST http://localhost:8002/find \
  -H "Content-Type: application/json" \
  -d '{"text": "The patient was admitted to St. Marys Hospital and assigned to room 204.", "labels": ["hospital", "room number"], "threshold": 0.0}')
echo "$RESPONSE"
assert_contains "$RESPONSE" "hospital" "hospitals: hospital label present"
assert_contains "$RESPONSE" "room" "hospitals: room number label present"
echo

echo "Testing medical_conditions (port 8003)..."
RESPONSE=$(curl -s -X POST http://localhost:8003/find \
  -H "Content-Type: application/json" \
  -d '{"text": "The patient was diagnosed with diabetes and hypertension.", "labels": ["DISEASE_DISORDER"], "threshold": 0.0}')
echo "$RESPONSE"
assert_contains "$RESPONSE" "diabetes" "medical_conditions: diabetes detected"
assert_contains "$RESPONSE" "hypertension" "medical_conditions: hypertension detected"
echo

echo "Testing french_persons (port 8004)..."
RESPONSE=$(curl -s -X POST http://localhost:8004/find \
  -H "Content-Type: application/json" \
  -d '{"text": "Jean Dupont est arrivé à Paris hier soir.", "labels": ["person"], "threshold": 0.0}')
echo "$RESPONSE"
assert_contains "$RESPONSE" "Jean Dupont" "french_persons: person detected"
echo

echo "Testing french_medical (port 8005)..."
RESPONSE=$(curl -s -X POST http://localhost:8005/find \
  -H "Content-Type: application/json" \
  -d '{"text": "Le patient souffre de diabète et d'\''hypertension artérielle.", "labels": ["Maladie"], "threshold": 0.3}')
echo "$RESPONSE"
assert_contains "$RESPONSE" "diab" "french_medical: diabète detected"
assert_contains "$RESPONSE" "hypertension" "french_medical: hypertension detected"
echo
