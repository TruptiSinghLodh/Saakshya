# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import face_recognition.api as face_recognition
import PIL.Image
import numpy as np
import pickle
import cv2


# 🔹 Get image files
def image_files_in_folder(folder):
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if re.match(r'.*\.(jpg|jpeg|png)', f, flags=re.I)
    ]


# 🔹 TRAINING FUNCTION
def scan_known_people(known_people_folder):
    known_names = []
    known_face_encodings = []

    for person_name in os.listdir(known_people_folder):
        person_folder = os.path.join(known_people_folder, person_name)

        if not os.path.isdir(person_folder):
            continue

        for file in image_files_in_folder(person_folder):
            basename = person_name
            img = face_recognition.load_image_file(file)
            encodings = face_recognition.face_encodings(img)

            if len(encodings) > 1:
                print(f"WARNING: More than one face found in {file}. Using first.")

            if len(encodings) == 0:
                print(f"WARNING: No face found in {file}. Skipping.")
                continue

            # 🔥 FIX: enforce correct dtype
            encoding = np.array(encodings[0], dtype=np.float64)

            known_names.append(basename)
            known_face_encodings.append(encoding)

    return known_names, known_face_encodings


# 🔹 SAVE MODEL
def train_face_encodings(dataset_path, encodings_path):
    known_names, known_face_encodings = scan_known_people(dataset_path)

    if len(known_names) == 0:
        return {"success": False, "message": "No faces found in dataset"}

    # 🔥 ensure all encodings are proper arrays
    known_face_encodings = [np.array(enc, dtype=np.float64) for enc in known_face_encodings]

    with open(encodings_path, "wb") as f:
        pickle.dump((known_names, known_face_encodings), f)

    return {
        "success": True,
        "message": f"Training complete with {len(known_names)} samples"
    }


# 🔹 RECOGNITION FUNCTION
def recognize_face(frame, encodings_path, tolerance=0.6):
    if not os.path.exists(encodings_path):
        return None, None

    # Load known faces
    with open(encodings_path, "rb") as f:
        known_names, known_face_encodings = pickle.load(f)

    # 🔥 FIX: enforce dtype again after loading
    known_face_encodings = [np.array(enc, dtype=np.float64) for enc in known_face_encodings]

    if len(known_face_encodings) == 0:
        return "unknown_person", None

    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize large frames
    if max(rgb_frame.shape) > 1600:
        pil_img = PIL.Image.fromarray(rgb_frame)
        pil_img.thumbnail((1600, 1600), PIL.Image.LANCZOS)
        rgb_frame = np.array(pil_img)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame)

    if len(face_encodings) == 0:
        return "no_persons_found", None

    # 🔥 FIX: enforce dtype for unknown faces
    face_encodings = [np.array(enc, dtype=np.float64) for enc in face_encodings]

    for face_encoding, face_location in zip(face_encodings, face_locations):

        # 🔥 SAFE distance calculation
        distances = face_recognition.face_distance(
            np.array(known_face_encodings),
            np.array(face_encoding)
        )

        if len(distances) == 0:
            return "unknown_person", face_location

        matches = list(distances <= tolerance)

        if True in matches:
            best_match_index = np.argmin(distances)
            return known_names[best_match_index], face_location
        else:
            return "unknown_person", face_location

    return None, None