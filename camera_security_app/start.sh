#!/bin/bash

echo "==================================="
echo "Camera Security Management System"
echo "==================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "สร้าง virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "เปิดใช้งาน virtual environment..."
source venv/bin/activate

# Install requirements
echo "ติดตั้ง dependencies..."
pip install -q -r requirements.txt

# Check for OpenSSL
if ! command -v openssl &> /dev/null; then
    echo "⚠️  OpenSSL ไม่ได้ติดตั้ง"
    echo "Ubuntu/Debian: sudo apt install openssl"
    echo "macOS: brew install openssl"
fi

# Check for FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg ไม่ได้ติดตั้ง (ตัวเลือก)"
    echo "Ubuntu/Debian: sudo apt install ffmpeg"
    echo "macOS: brew install ffmpeg"
fi

echo ""
echo "เริ่มต้นระบบ..."
echo "เปิดเบราว์เซอร์ไปที่: http://localhost:5000"
echo ""

# Start Flask app
python app.py
