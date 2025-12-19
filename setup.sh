#!/bin/bash

# Setup script for Sentient Vision Property Intelligence Platform
# This script will set up both frontend and backend development environments

set -e  # Exit on any error

echo "🏠 Setting up Sentient Vision - Premium Property Intelligence Platform"
echo "=================================================================="

# Check if we're in the correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the PropertyIntel directory"
    exit 1
fi

# Check for Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first:"
    echo "   macOS: brew install node"
    echo "   Or download from: https://nodejs.org/"
    exit 1
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first:"
    echo "   macOS: brew install python"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Setup Backend
echo ""
echo "🔧 Setting up FastAPI Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Backend setup complete!"

# Setup Frontend
echo ""
echo "🎨 Setting up Vue.js Frontend..."
cd ../frontend

# Install npm dependencies
echo "📥 Installing Node.js dependencies..."
npm install

# Install additional Tailwind CSS plugins
echo "🎨 Installing Tailwind CSS plugins..."
npm install -D @tailwindcss/forms @tailwindcss/typography

echo "✅ Frontend setup complete!"

# Back to root directory
cd ..

# Create environment files
echo ""
echo "⚙️  Creating environment configuration..."

# Backend .env
if [ ! -f "backend/.env" ]; then
    cat > backend/.env << EOF
DATABASE_URL=sqlite:///./property_intel.db
SECRET_KEY=your-secret-key-change-in-production-$(openssl rand -hex 32)
ACCESS_TOKEN_EXPIRE_MINUTES=30
EOF
    echo "✅ Created backend/.env"
fi

# Frontend .env
if [ ! -f "frontend/.env" ]; then
    cat > frontend/.env << EOF
VITE_API_BASE_URL=http://localhost:8000/api
EOF
    echo "✅ Created frontend/.env"
fi

# Create start scripts
echo ""
echo "🚀 Creating start scripts..."

# Backend start script
cat > start-backend.sh << 'EOF'
#!/bin/bash
echo "🔧 Starting FastAPI Backend..."
cd backend
source venv/bin/activate
python main.py
EOF
chmod +x start-backend.sh

# Frontend start script
cat > start-frontend.sh << 'EOF'
#!/bin/bash
echo "🎨 Starting Vue.js Frontend..."
cd frontend
npm run dev
EOF
chmod +x start-frontend.sh

# Combined start script
cat > start-dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting Sentient Vision Development Environment..."
echo "Backend will start on: http://localhost:8000"
echo "Frontend will start on: http://localhost:3000"
echo ""

# Start backend in background
./start-backend.sh &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend in background
./start-frontend.sh &
FRONTEND_PID=$!

echo "✅ Both servers started!"
echo "📊 Backend API: http://localhost:8000"
echo "🎨 Frontend App: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers..."

# Wait for interrupt
wait

# Cleanup
echo "🛑 Stopping servers..."
kill $BACKEND_PID 2>/dev/null || true
kill $FRONTEND_PID 2>/dev/null || true
echo "✅ Servers stopped"
EOF
chmod +x start-dev.sh

echo ""
echo "🎉 Setup Complete!"
echo "=================================================================="
echo ""
echo "🚀 To start the development environment:"
echo "   ./start-dev.sh"
echo ""
echo "🔧 To start only the backend:"
echo "   ./start-backend.sh"
echo ""
echo "🎨 To start only the frontend:"
echo "   ./start-frontend.sh"
echo ""
echo "📱 Access the application:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Documentation: http://localhost:8000/docs"
echo ""
echo "📖 For more information, see README.md"
echo ""
echo "Happy coding! 🏠✨"