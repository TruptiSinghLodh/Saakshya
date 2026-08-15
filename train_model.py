import os
import cv2
import pickle
import numpy as np

dataset_path = "dataset"
encodings = []
names = []

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

print("🔄 Training started...\n")

def preprocess(img):
    # Improve lighting automatically
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    return gray

for person in os.listdir(dataset_path):
    person_path = os.path.join(dataset_path, person)

    if not os.path.isdir(person_path):
        continue

    print(f"📂 Processing: {person}")

    for img_name in os.listdir(person_path):
        img_path = os.path.join(person_path, img_name)

        try:
            img = cv2.imread(img_path)

            if img is None:
                print(f"❌ Cannot read: {img_name}")
                continue

            gray = preprocess(img)

            # 🔥 Try multiple detection settings
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)

            if len(faces) == 0:
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            if len(faces) == 0:
                faces = face_cascade.detectMultiScale(gray, 1.05, 3)

            if len(faces) == 0:
                print(f"⚠ No face: {img_name}")
                continue

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face = cv2.resize(face, (100, 100))

                encodings.append(face.flatten())
                names.append(person)

        except Exception as e:
            print(f"❌ Error: {img_name} → {e}")

# Save model
with open("encodings.pkl", "wb") as f:
    pickle.dump((encodings, names), f)

print("\n✅ Training Complete!")
print(f"📊 Faces trained: {len(encodings)}")