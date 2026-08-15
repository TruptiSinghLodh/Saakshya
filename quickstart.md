# 🎓 QUICK START GUIDE

## Installation (First Time Only)

```bash
cd /app/flask_attendance

# Install Python dependencies
pip install -r requirements.txt
```

## Running the Application

### Method 1: Direct Run
```bash
python app.py
```

### Method 2: Using Start Script
```bash
chmod +x start.sh
./start.sh
```

### Method 3: Using Quick Run
```bash
chmod +x run.sh
./run.sh
```

The application will start on: **http://localhost:5000**

---

## Step-by-Step Usage

### 1️⃣ Register Students

1. Open browser → Go to `http://localhost:5000`
2. Click **"Register Student"**
3. Enter student name
4. Click **"Start Camera"**
5. Click **"Capture Image"** 15 times
   - Take from different angles
   - Vary expressions slightly
   - Ensure good lighting
6. Click **"Register Student"**
7. Repeat for all students

### 2️⃣ Train the Model

1. After registering all students
2. Click **"Train Model"** button
3. Wait for training to complete
4. You'll see success message with number of students and images

### 3️⃣ Mark Attendance

1. Go to **"Mark Attendance"**
2. Click **"Start Scanning"**
3. Student faces camera
4. System checks:
   - ✅ Blink 2-3 times (anti-spoofing)
   - ✅ Move head slightly
5. Face recognized automatically
6. Attendance marked with emotion

### 4️⃣ View Analytics

1. Go to **"Analytics Dashboard"**
2. View:
   - Total students
   - Present today
   - Attendance percentage
   - Weekly trends (graph)
   - Most absent students
   - Late entries
   - Attendance records
3. Click **"Generate Report"** for daily summary

---

## 🎨 Features

- ✅ Face Recognition
- ✅ Liveness Detection (Blink + Head Movement)
- ✅ Emotion Analysis (Happy, Sad, Neutral, Sleepy)
- ✅ Proxy Detection
- ✅ Real-time Alerts
- ✅ Analytics Dashboard
- ✅ Weekly Trends
- ✅ Auto Reports

---

## 📁 File Structure

```
flask_attendance/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── README.md             # Full documentation
├── QUICKSTART.md         # This file
├── start.sh              # Startup script
├── run.sh                # Quick run script
│
├── templates/            # HTML pages
├── static/               # CSS & JS
├── utils/                # Helper functions
│
├── dataset/              # Student images (auto-created)
├── reports/              # Generated reports (auto-created)
├── encodings.pkl         # Trained model (auto-created)
├── attendance.csv        # Attendance records (auto-created)
└── alerts.txt            # Alert logs (auto-created)
```

---

## 🐛 Troubleshooting

### Camera not working?
- Allow camera permissions in browser
- Close other apps using camera
- Use Chrome or Firefox

### Face not recognized?
- Ensure model is trained
- Check lighting
- Re-register with more varied images

### Liveness check failing?
- Blink naturally (not too fast)
- Make small head movements
- Look directly at camera

---

## 💡 Tips

- **Good Lighting**: Ensure face is well-lit
- **Camera Distance**: Stay 2-3 feet from camera
- **Multiple Angles**: Capture images from different angles during registration
- **Regular Updates**: Train model after adding new students

---

## 📞 Need Help?

Check the full README.md for detailed documentation.

---

**Built with ❤️ for Smart Classrooms**