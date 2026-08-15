from flask import Flask, render_template, request, jsonify, Response
import cv2
import pickle
import os
import pandas as pd
from datetime import datetime, timedelta
import json
from utils.emotion_detection import detect_emotion
from utils.liveness_detection import LivenessDetector
from utils.face_recognition_utils import train_face_encodings, recognize_face
import numpy as np

app = Flask(__name__)

# Configuration
DATASET_PATH = 'dataset'
ENCODINGS_PATH = 'encodings.pkl'
ATTENDANCE_CSV = 'attendance.csv'
ALERTS_FILE = 'alerts.txt'
REPORTS_PATH = 'reports'

# Initialize liveness detector
liveness_detector = LivenessDetector()

# Create necessary directories
for path in [DATASET_PATH, REPORTS_PATH]:
    os.makedirs(path, exist_ok=True)

# Initialize CSV if not exists
if not os.path.exists(ATTENDANCE_CSV):
    df = pd.DataFrame(columns=['Name', 'Date', 'Time', 'Emotion', 'Status'])
    df.to_csv(ATTENDANCE_CSV, index=False)

# Initialize alerts file
if not os.path.exists(ALERTS_FILE):
    with open(ALERTS_FILE, 'w') as f:
        f.write('')


@app.route('/')
def index():
    """Home page with navigation"""
    return render_template('index.html')


@app.route('/register')
def register():
    """Student registration page"""
    return render_template('register.html')


@app.route('/scan')
def scan():
    """Face scanning page"""
    return render_template('scan.html')


@app.route('/dashboard')
def dashboard():
    """Analytics dashboard"""
    return render_template('dashboard.html')


@app.route('/api/save_student', methods=['POST'])
def save_student():
    """Save student images for registration"""
    try:
        data = request.json
        student_name = data.get('name', '').strip()
        images_data = data.get('images', [])

        if not student_name or len(images_data) < 15:
            return jsonify({'success': False, 'message': 'Need at least 15 images'})

        # Create student directory
        student_path = os.path.join(DATASET_PATH, student_name)
        os.makedirs(student_path, exist_ok=True)

        # Save images
        for idx, img_data in enumerate(images_data):
            # Decode base64 image
            import base64
            img_bytes = base64.b64decode(img_data.split(',')[1])
            img_array = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

            # Save image
            img_path = os.path.join(student_path, f'{idx+1}.jpg')
            cv2.imwrite(img_path, img)

        return jsonify({'success': True, 'message': f'{student_name} registered with {len(images_data)} images'})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/train_model', methods=['POST'])
def train_model():
    """Train face recognition model"""
    try:
        result = train_face_encodings(DATASET_PATH, ENCODINGS_PATH)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/recognize_face', methods=['POST'])
def recognize_face_api():
    # NOTE: liveness (blink_count / head_movement) is still trusted from the
    # client here. This is the fix we discussed but haven't implemented yet —
    # share utils/liveness_detection.py and we'll rewrite this properly to
    # verify liveness from the frame itself, server-side.
    try:
        data = request.json
        frame_data = data.get('frame')
        blink_count = data.get('blink_count', 0)
        head_movement = data.get('head_movement', False)

        # Decode base64 image
        import base64
        img_bytes = base64.b64decode(frame_data.split(',')[1])
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # Check if encodings exist
        if not os.path.exists(ENCODINGS_PATH):
            return jsonify({'success': False, 'message': 'Model not trained yet'})

        # Recognize face using our custom function
        name, face_location = recognize_face(frame, ENCODINGS_PATH)

        if name is None or name == "Unknown":
            return jsonify({'success': False, 'message': 'Face not recognized'})

        # Check liveness (2-3 blinks required + head movement)
        if blink_count < 2:
            return jsonify({'success': False, 'message': f'Liveness check failed. Blink more (detected: {blink_count})', 'name': name})

        if not head_movement:
            return jsonify({'success': False, 'message': 'Please move your head slightly', 'name': name})

        # Detect emotion
        try:
            emotion = detect_emotion(frame)
        except:
            emotion = 'Neutral 😐'

        # Check for proxy (duplicate attendance today)
        today = datetime.now().strftime('%Y-%m-%d')
        df = pd.read_csv(ATTENDANCE_CSV)

        if not df.empty:
            today_attendance = df[(df['Name'] == name) & (df['Date'] == today)]
            if not today_attendance.empty:
                # Check if marked within last 1 hour (proxy detection)
                last_time = today_attendance.iloc[-1]['Time']
                last_datetime = datetime.strptime(f"{today} {last_time}", '%Y-%m-%d %H:%M:%S')
                time_diff = datetime.now() - last_datetime

                if time_diff.total_seconds() < 3600:  # 1 hour
                    log_alert(f"PROXY ALERT: {name} tried to mark attendance again within 1 hour")
                    return jsonify({'success': False, 'message': 'Attendance already marked recently (Proxy detected)'})

        # Mark attendance
        current_time = datetime.now()
        new_entry = pd.DataFrame([{
            'Name': name,
            'Date': current_time.strftime('%Y-%m-%d'),
            'Time': current_time.strftime('%H:%M:%S'),
            'Emotion': emotion,
            'Status': 'Present'
        }])

        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(ATTENDANCE_CSV, index=False)

        # Log alert
        log_alert(f"{name} marked present at {current_time.strftime('%H:%M:%S')} - Emotion: {emotion}")

        return jsonify({
            'success': True,
            'name': name,
            'emotion': emotion,
            'time': current_time.strftime('%H:%M:%S'),
            'message': f'Attendance marked for {name}'
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/get_analytics', methods=['GET'])
def get_analytics():
    """Get attendance analytics"""
    try:
        if not os.path.exists(ATTENDANCE_CSV):
            return jsonify({'success': False, 'message': 'No attendance data'})

        df = pd.read_csv(ATTENDANCE_CSV)

        # Get REGISTERED students (not just students who've attended) —
        # this is the source of truth for total_students and for the
        # "most absent" list below, so a student with 0% attendance still
        # shows up instead of being invisible.
        if os.path.exists(DATASET_PATH):
            unique_students = [d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))]
        else:
            unique_students = []
        total_students = len(unique_students)

        if df.empty:
            return jsonify({
                'success': True,
                'total_students': total_students,
                'present_today': 0,
                'attendance_percentage': 0,
                'weekly_data': [],
                'most_absent': [{'name': s, 'absent_days': 0} for s in unique_students[:5]],
                'late_entries': [],
                'records': []
            })

        # (Removed: the old CSV-based re-derivation of unique_students/total_students
        # that used to sit here and silently overwrite the fix above — that was the bug.)

        # Today's attendance
        today = datetime.now().strftime('%Y-%m-%d')
        today_df = df[df['Date'] == today]
        present_today = len(today_df['Name'].unique())
        attendance_percentage = (present_today / total_students * 100) if total_students > 0 else 0

        # Weekly data (last 7 days)
        weekly_data = []
        for i in range(6, -1, -1):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            day_df = df[df['Date'] == date]
            day_present = len(day_df['Name'].unique())
            day_percentage = (day_present / total_students * 100) if total_students > 0 else 0
            weekly_data.append({
                'date': date,
                'percentage': round(day_percentage, 1),
                'present': day_present
            })

        # Most absent students
        attendance_count = df.groupby('Name')['Date'].nunique().to_dict()
        total_days = df['Date'].nunique()
        absent_data = []
        for student in unique_students:
            present_days = attendance_count.get(student, 0)
            absent_days = total_days - present_days
            absent_data.append({'name': student, 'absent_days': absent_days})

        most_absent = sorted(absent_data, key=lambda x: x['absent_days'], reverse=True)[:5]

        # Late entries (after 9:30 AM)
        late_entries = []
        for _, row in today_df.iterrows():
            time_obj = datetime.strptime(row['Time'], '%H:%M:%S').time()
            if time_obj > datetime.strptime('09:30:00', '%H:%M:%S').time():
                late_entries.append({
                    'name': row['Name'],
                    'time': row['Time']
                })

        # Recent records
        records = df.tail(20).to_dict('records')
        records.reverse()

        return jsonify({
            'success': True,
            'total_students': total_students,
            'present_today': present_today,
            'attendance_percentage': round(attendance_percentage, 1),
            'weekly_data': weekly_data,
            'most_absent': most_absent,
            'late_entries': late_entries,
            'records': records
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/get_alerts', methods=['GET'])
def get_alerts():
    """Get recent alerts"""
    try:
        if not os.path.exists(ALERTS_FILE):
            return jsonify({'success': True, 'alerts': []})

        with open(ALERTS_FILE, 'r') as f:
            alerts = f.readlines()[-20:]  # Last 20 alerts

        alerts.reverse()
        return jsonify({'success': True, 'alerts': [a.strip() for a in alerts]})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/generate_report', methods=['POST'])
def generate_report():
    """Generate daily attendance report"""
    try:
        date = request.json.get('date', datetime.now().strftime('%Y-%m-%d'))

        df = pd.read_csv(ATTENDANCE_CSV)
        date_df = df[df['Date'] == date]

        # Get all students
        all_students = df['Name'].unique().tolist()
        present_students = date_df['Name'].unique().tolist()
        absent_students = [s for s in all_students if s not in present_students]

        # Generate report
        report = f"""DAILY ATTENDANCE REPORT
Date: {date}
{'='*50}

Total Students: {len(all_students)}
Present: {len(present_students)}
Absent: {len(absent_students)}
Attendance %: {len(present_students)/len(all_students)*100:.1f}%

{'='*50}
PRESENT STUDENTS:
{'='*50}
"""
        for _, row in date_df.iterrows():
            report += f"{row['Name']:<20} {row['Time']:<10} {row['Emotion']:<15}\n"

        report += f"\n{'='*50}\nABSENT STUDENTS:\n{'='*50}\n"
        for student in absent_students:
            report += f"{student}\n"

        # Save report
        # encoding='utf-8' is required here because emotion values contain
        # emoji (e.g. 'Neutral 😐') — Windows' default file encoding (cp1252)
        # can't represent those characters and raises a UnicodeEncodeError.
        report_file = os.path.join(REPORTS_PATH, f'report_{date}.txt')
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        return jsonify({'success': True, 'message': f'Report generated: {report_file}', 'report': report})

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/get_students', methods=['GET'])
def get_students():
    """Get list of registered students"""
    try:
        students = []
        if os.path.exists(DATASET_PATH):
            students = [d for d in os.listdir(DATASET_PATH) if os.path.isdir(os.path.join(DATASET_PATH, d))]
        return jsonify({'success': True, 'students': students, 'count': len(students)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


def log_alert(message):
    """Log alert to file"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ALERTS_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)