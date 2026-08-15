"# 🎓 Smart Classroom Face Recognition Attendance System

An advanced AI-powered attendance system with face recognition, liveness detection, emotion analysis, and comprehensive analytics.

## ✨ Features

### Core Features
- 👤 **Student Registration**: Register students with 15 face images for accurate recognition
- 🎥 **Real-time Face Recognition**: Automatic face detection and identification
- 👁️ **Anti-Spoofing**: Liveness detection through blink and head movement verification
- 😊 **Emotion Detection**: Tracks student emotions (Happy, Sad, Neutral, Sleepy)
- ✅ **Automatic Attendance**: Marks attendance with timestamp and emotion

### Advanced Features
- 📊 **Analytics Dashboard**: 
  - Daily and weekly attendance trends
  - Student engagement analysis
  - Most absent students tracking
  - Late entry monitoring
- 🚨 **Proxy Detection**: Prevents duplicate attendance within 1 hour
- 🔔 **Real-time Alerts**: Teacher notifications for attendance events
- 📄 **Auto Report Generation**: Daily attendance reports in text format
- 📈 **Interactive Charts**: Visual attendance analytics using Chart.js

## 🛠️ Technologies Used

- **Backend**: Flask (Python 3.11+)
- **Computer Vision**: OpenCV
- **Face Recognition**: OpenCV DNN + Histogram Comparison
- **Emotion Detection**: FER (Facial Emotion Recognition)
- **Data Management**: Pandas
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Charts**: Chart.js

## 📋 Requirements

- Python 3.11 or higher
- Webcam/Camera
- Modern web browser (Chrome, Firefox, Safari)

## 🚀 Installation

1. **Clone or download the project**
   ```bash
   cd /app/flask_attendance
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   This will install:
   - Flask
   - OpenCV (opencv-python, opencv-contrib-python)
   - Pandas
   - FER (Facial Emotion Recognition)
   - NumPy, SciPy, Pillow, imutils

## 🎯 Usage

### Step 1: Start the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 2: Register Students

1. Open browser and go to `http://localhost:5000`
2. Click **\"Register Student\"**
3. Enter student's full name
4. Click **\"Start Camera\"** to activate webcam
5. Click **\"Capture Image\"** 15 times
   - Take pictures from different angles
   - Vary facial expressions slightly
   - Ensure good lighting
6. Click **\"Register Student\"** to save
7. Repeat for all students

### Step 3: Train the Model

1. After registering all students, click **\"Train Model\"**
2. Wait for training to complete (may take a few minutes)
3. Success message will confirm training completion

### Step 4: Mark Attendance

1. Go to **\"Mark Attendance\"** page
2. Click **\"Start Scanning\"**
3. Student faces the camera
4. System performs liveness checks:
   - **Blink Detection**: Student must blink 2-3 times
   - **Head Movement**: Student should move head slightly
5. Once verified, face is recognized
6. Attendance is automatically marked with:
   - Student name
   - Current time
   - Detected emotion
   - Status

### Step 5: View Analytics

1. Go to **\"Analytics Dashboard\"**
2. View comprehensive analytics:
   - Total students and present today
   - Attendance percentage
   - Weekly attendance trends (chart)
   - Most absent students
   - Late entries today
   - Recent attendance records
3. Click **\"Generate Report\"** for daily report

## 📁 Project Structure

```
flask_attendance/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── encodings.pkl               # Trained face encodings (generated)
├── attendance.csv             # Attendance records (generated)
├── alerts.txt                 # Alert logs (generated)
│
├── dataset/                   # Student face images
│   └── [student_name]/
│       └── 1.jpg, 2.jpg, ...
│
├── reports/                   # Generated reports
│   └── report_YYYY-MM-DD.txt
│
├── templates/                 # HTML templates
│   ├── index.html            # Home page
│   ├── register.html         # Student registration
│   ├── scan.html            # Face scanning
│   └── dashboard.html       # Analytics dashboard
│
├── static/                    # Static assets
│   ├── css/
│   │   └── style.css        # Modern green/mint theme
│   └── js/
│       ├── camera.js        # Camera handling
│       └── charts.js        # Dashboard analytics
│
└── utils/                     # Utility modules
    ├── face_recognition_utils.py
    ├── emotion_detection.py
    └── liveness_detection.py
```

## 🎨 Design

The application features a modern **Green/Mint Pastel** theme with:
- Soft, eye-friendly colors
- Smooth animations and transitions
- Responsive design
- Clean, professional interface
- Glassmorphism effects

## 🔒 Security Features

1. **Liveness Detection**: 
   - Blink detection (minimum 2 blinks)
   - Head movement verification
   - Prevents photo/video spoofing

2. **Proxy Detection**:
   - Prevents same person marking attendance twice within 1 hour
   - Logs suspicious activities

3. **Face Verification**:
   - Multi-image training (15 images per student)
   - Histogram-based face matching
   - Confidence threshold validation

## 📊 Analytics Features

### Dashboard Metrics
- **Total Students**: Count of registered students
- **Present Today**: Students who marked attendance today
- **Attendance Rate**: Percentage of present students
- **Late Entries**: Students arriving after 9:30 AM

### Visualizations
- **Weekly Trend Chart**: 7-day attendance percentage graph
- **Most Absent Students**: Top 5 students with most absences
- **Real-time Alerts**: Recent attendance events
- **Attendance Table**: Detailed records with emotions

### Reports
- Daily summary reports
- Present/absent student lists
- Emotion analysis
- Time-stamped records

## 🐛 Troubleshooting

### Camera Not Working
- **Browser permissions**: Allow camera access when prompted
- **Multiple apps**: Close other apps using the camera
- **Browser compatibility**: Use Chrome or Firefox for best results

### Face Not Recognized
- **Training**: Ensure model is trained after registration
- **Lighting**: Ensure good, even lighting on face
- **Distance**: Maintain 2-3 feet from camera
- **Re-register**: Try re-registering with more varied images

### Liveness Check Failing
- **Blink naturally**: Don't force blinks too fast
- **Head movement**: Make small, natural head movements
- **Look at camera**: Ensure face is clearly visible

### Installation Issues
- **OpenCV**: If opencv-python fails, try: `pip install opencv-python-headless`
- **FER**: If FER fails, try: `pip install fer --no-deps` then install dependencies manually
- **Permissions**: Run terminal/command prompt as administrator

## 🔄 How It Works

### Face Recognition Process
1. **Training Phase**:
   - Load all student images from dataset
   - Detect faces using Haar Cascade
   - Extract face features (histogram)
   - Save encodings to pickle file

2. **Recognition Phase**:
   - Capture frame from camera
   - Detect face in frame
   - Extract face features
   - Compare with stored encodings
   - Match face using correlation

### Liveness Detection
1. **Blink Detection**:
   - Use Haar Cascade for eye detection
   - Count frames where eyes disappear
   - Require 2-3 consecutive blinks

2. **Head Movement**:
   - Compare face position across frames
   - Calculate pixel displacement
   - Verify movement > 5 pixels

### Emotion Detection
1. Use FER library for emotion recognition
2. Detect 7 emotions: Happy, Sad, Angry, Neutral, Fear, Surprise, Disgust
3. Map to 4 categories: Happy 🙂, Sad 😞, Neutral 😐, Sleepy 😴
4. Store emotion with attendance record

## 🎓 Educational Use

This project is perfect for:
- Computer Science final year projects
- AI/ML course assignments
- Face recognition learning
- Computer vision applications
- Python Flask web development

## 📝 Notes

- **Privacy**: Face images stored locally, not sent to cloud
- **Accuracy**: Dependent on image quality and lighting
- **Performance**: Works best with 5-20 students
- **Scalability**: For larger deployments, consider using dlib or face_recognition library

## 🚀 Future Enhancements

- [ ] Multi-face recognition (batch attendance)
- [ ] Mobile app integration
- [ ] Cloud backup
- [ ] Email/SMS notifications
- [ ] Stronger deep learning models
- [ ] Export to Excel
- [ ] Student performance correlation

## 📄 License

Free to use for educational and personal projects.

## 🤝 Support

For issues or questions:
1. Check troubleshooting section
2. Ensure all dependencies installed correctly
3. Verify camera permissions
4. Check console logs for errors

---

**Built with ❤️ for Smart Classrooms**
"