import cv2
import numpy as np
from scipy.spatial import distance as dist

class LivenessDetector:
    """
    Detects liveness through blink detection and head movement
    """
    
    def __init__(self):
        # Eye aspect ratio threshold
        self.EAR_THRESHOLD = 0.25
        self.CONSEC_FRAMES = 2
        
        # Load face and eye cascade classifiers
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        
        self.blink_counter = 0
        self.frame_counter = 0
    
    def eye_aspect_ratio(self, eye):
        """
        Calculate eye aspect ratio
        """
        # Compute the euclidean distances between the vertical eye landmarks
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        
        # Compute the euclidean distance between the horizontal eye landmarks
        C = dist.euclidean(eye[0], eye[3])
        
        # Compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        return ear
    
    def detect_blink(self, frame):
        """
        Detect if person blinked
        Returns: (blinked, blink_count)
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        blinked = False
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
            
            if len(eyes) == 0:
                # No eyes detected, might be blinking
                self.frame_counter += 1
                if self.frame_counter >= self.CONSEC_FRAMES:
                    self.blink_counter += 1
                    self.frame_counter = 0
                    blinked = True
            else:
                self.frame_counter = 0
        
        return blinked, self.blink_counter
    
    def detect_head_movement(self, prev_frame, curr_frame):
        """
        Detect head movement between frames
        """
        if prev_frame is None:
            return False
        
        # Convert to grayscale
        prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in both frames
        prev_faces = self.face_cascade.detectMultiScale(prev_gray, 1.3, 5)
        curr_faces = self.face_cascade.detectMultiScale(curr_gray, 1.3, 5)
        
        if len(prev_faces) == 0 or len(curr_faces) == 0:
            return False
        
        # Get first face location in each frame
        prev_x, prev_y, _, _ = prev_faces[0]
        curr_x, curr_y, _, _ = curr_faces[0]
        
        # Calculate movement
        movement = np.sqrt((curr_x - prev_x)**2 + (curr_y - prev_y)**2)
        
        # If movement is significant (more than 5 pixels)
        return movement > 5
    
    def reset(self):
        """Reset counters"""
        self.blink_counter = 0
        self.frame_counter = 0