#!/bin/bash

# Smart Classroom Attendance System - Startup Script

echo "==========================================="
echo "  Smart Classroom Attendance System"
echo "  Face Recognition with AI"
echo "==========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create necessary directories
mkdir -p dataset reports

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Starting Flask application..."
echo ""
echo "📱 Open your browser and go to:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Flask app
python app.py