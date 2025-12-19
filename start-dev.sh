#!/bin/bash

# PropertyIntel Development Server Startup Script
set -e

echo "🏠 Starting PropertyIntel Development Environment..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Load nvm if it exists
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required tools
echo "🔧 Checking dependencies..."

if ! command_exists python3; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

if ! command_exists npm; then
    echo -e "${RED}❌ Node.js/npm is required but not installed${NC}"
    echo "Please install Node.js from https://nodejs.org/ or use nvm"
    exit 1
fi

echo -e "${GREEN}✅ All dependencies found${NC}"

# Backend setup
echo -e "${BLUE}🔧 Setting up backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Starting FastAPI backend..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Frontend setup
echo -e "${BLUE}🔧 Setting up frontend...${NC}"
cd ../frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

echo "Starting Vue.js frontend..."
npm run dev &
FRONTEND_PID=$!

# Wait for servers to start
echo -e "${GREEN}⏳ Waiting for servers to start...${NC}"
sleep 5

echo ""
echo -e "${GREEN}✅ PropertyIntel is now running!${NC}"
echo "📊 Backend API: http://localhost:8000"
echo "🎨 Frontend App: http://localhost:5173"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${BLUE}🛑 Stopping servers...${NC}"
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo -e "${GREEN}✅ Servers stopped${NC}"
    exit 0
}

# Set trap for cleanup
trap cleanup INT TERM

# Wait for interrupt
wait
