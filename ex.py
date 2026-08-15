import face_recognition

img = face_recognition.load_image_file("img1.jpg")
faces = face_recognition.face_locations(img)

print(faces)