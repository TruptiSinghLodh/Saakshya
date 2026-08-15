#!/bin/bash

# Quick start without virtual environment
echo "🚀 Starting Smart Classroom Attendance System..."
echo ""

# Create necessary directories
mkdir -p dataset reports

echo "📱 Server starting at http://localhost:5000"
echo "Press Ctrl+C to stop"
echo ""

python app.py