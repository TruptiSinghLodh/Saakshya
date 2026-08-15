import cv2
import random

def detect_emotion(frame):
    
    #Detect emotion from face in frame
    #Returns: emotion string (Happy, Sad, Neutral, Sleepy, etc.)
    
    #Simplified version using facial feature analysis
    #For production, integrate with TensorFlow emotion model
    
    try:
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Load face cascade
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
        # Detect face
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        if len(faces) == 0:
            return 'Neutral 😐'
        
        # Get first face
        (x, y, w, h) = faces[0]
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detect eyes
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        
        # Detect smile
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
        
        # Simple emotion logic
        if len(smiles) > 0:
            return 'Happy 🙂'
        elif len(eyes) < 2:
            # Eyes not fully detected, might be sleepy or sad
            return 'Sleepy 😴'
        else:
            # Default to neutral
            emotions = ['Neutral 😐', 'Neutral 😐', 'Neutral 😐', 'Sad 😞']
            return random.choice(emotions)  # Slight randomness for demo
    
    except Exception as e:
        return 'Neutral 😐'
