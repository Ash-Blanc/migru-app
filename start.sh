#!/bin/bash

echo "🚀 Starting MIGRU V2..."
echo ""

# Check if database exists, initialize if not
if [ ! -f "src/backend/migru.db" ]; then
    echo "📊 Initializing database..."
    cd src/backend
    uv run python -c "from app.database import init_db; init_db()"
    cd ../..
fi

# Check for .env file
if [ ! -f "src/backend/.env" ]; then
    echo "⚠️  No .env file found. Creating default..."
    cat > src/backend/.env << EOF
DEV_MODE=true
CLERK_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
HUME_API_KEY=
HUME_SECRET_KEY=
EOF
    echo "✅ Created .env with DEV_MODE=true"
fi

# Start backend in background
echo "🔧 Starting backend on port 8000..."
cd src/backend
uv run uvicorn app.main_v2:app --reload --port 8000 &
BACKEND_PID=$!
cd ../..

# Wait for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend on port 5173..."
cd src/frontend
npm run dev &
FRONTEND_PID=$!
cd ../..

echo ""
echo "✅ MIGRU V2 is running!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend:  http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Trap Ctrl+C to kill both processes
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
