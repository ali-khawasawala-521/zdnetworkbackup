#!/bin/bash

APP_MODULE="main:app"
BACKEND_DIR="backend"
FRONTEND_DIR="frontend"
HOST="0.0.0.0"
PORT="6666"
DEV=false

# Parse dev argument for backend and frontend
if [ "$1" == "--dev" ] || [ "$1" == "-r" ]; then
    DEV=true
fi

echo "🚀 Starting ZD Network Backup ..."
echo "Starting Backend on http://${HOST}:${PORT} with reload=${DEV} ..."

# Activate venv
source ./backend/venv/bin/activate

if [ "$RELOAD" = true ]; then
    uvicorn "backend.$APP_MODULE" --host "$HOST" --port "$PORT" --reload &
else
    uvicorn "backend.$APP_MODULE" --host "$HOST" --port "$PORT" &
fi
BACKEND_PID=$!

# Start frontend
echo "Starting Frontend on http://${HOST}:${VUE_PORT} ..."
cd "$FRONTEND_DIR" || { echo "Frontend directory not found!"; kill $BACKEND_PID; exit 1; }

if [ "$DEV" = true ]; then
    npm run dev &
    FRONTEND_PID=$!
else
    npm run build && npm run preview
fi

# Wait for both processes to finish
wait $BACKEND_PID $FRONTEND_PID
