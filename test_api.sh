#!/bin/bash

echo "🧪 MIGRU V2 API Test Suite"
echo "Testing backend at http://localhost:8000"
echo ""

TOKEN="dev_token"
API="http://localhost:8000"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

test_endpoint() {
    local name=$1
    local method=$2
    local endpoint=$3
    local data=$4

    echo -n "Testing $name... "

    if [ -z "$data" ]; then
        response=$(curl -s -w "\n%{http_code}" -X $method "$API$endpoint" -H "Authorization: Bearer $TOKEN" 2>&1)
    else
        response=$(curl -s -w "\n%{http_code}" -X $method "$API$endpoint" \
            -H "Authorization: Bearer $TOKEN" \
            -H "Content-Type: application/json" \
            -d "$data" 2>&1)
    fi

    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n -1)

    if [ "$http_code" = "200" ]; then
        echo -e "${GREEN}✓ OK${NC} ($http_code)"
        return 0
    else
        echo -e "${RED}✗ FAIL${NC} ($http_code)"
        echo "Response: $body"
        return 1
    fi
}

echo "=== Health Check ==="
test_endpoint "Health" "GET" "/health"
echo ""

echo "=== User Status ==="
test_endpoint "Get Status" "GET" "/api/status"
echo ""

echo "=== Forecasting ==="
test_endpoint "Get Forecast" "GET" "/api/forecast"
echo ""

echo "=== Logging ==="
test_endpoint "Log Attack" "POST" "/api/logs" '{
  "severity": 7,
  "primary_symptoms": ["Nausea", "Light Sensitivity"],
  "triggers": ["Stress"],
  "notes": "Test attack from API test suite"
}'
test_endpoint "Get Logs" "GET" "/api/logs?limit=3"
echo ""

echo "=== Voice Analysis ==="
test_endpoint "Voice Trend" "GET" "/api/voice/trend?days=7"
echo ""

echo "=== Interventions ==="
test_endpoint "Start Intervention" "POST" "/api/interventions" '{
  "context": {"stress_score": 75}
}'
test_endpoint "Get Best Interventions" "GET" "/api/interventions/best"
echo ""

echo "=== Analytics ==="
test_endpoint "Get Analytics" "GET" "/api/analytics"
echo ""

echo "=== Hume Integration ==="
test_endpoint "Hume Auth" "GET" "/hume/auth"
test_endpoint "Hume Tools" "GET" "/hume/tools"
echo ""

echo "=== Onboarding ==="
test_endpoint "Onboarding Status" "GET" "/api/onboarding/status"
echo ""

echo "=== Pattern Recognition ==="
test_endpoint "Model Performance" "GET" "/api/patterns/performance?days=30"
echo ""

echo ""
echo "🎉 Test suite complete!"
echo ""
echo "Next steps:"
echo "1. Check frontend at http://localhost:5173"
echo "2. Visit /analytics to see KPI dashboard"
echo "3. Visit /onboarding to see the flow"
echo "4. Check API docs at http://localhost:8000/docs"
