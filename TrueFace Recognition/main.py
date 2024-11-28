#Wait a moment for the camera to open.

import cv2
import os
import numpy as np
from PIL import Image

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
known_faces = []
known_names = []

images_path = "images/"
valid_extensions = ('.jpg', '.jpeg', '.png')

if not os.path.exists(images_path):
    print(f"Error: The directory '{images_path}' does not exist.")
else:
    print(f"Directory '{images_path}' exists.")
    files = os.listdir(images_path)
    if not files:
        print("Error: The directory is empty.")
    else:
        print("Loading images for face recognition...")
        for file_name in files:
            if file_name.lower().endswith(valid_extensions):
                img_path = os.path.join(images_path, file_name)
                try:
                    pil_image = Image.open(img_path)
                    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                    for (x, y, w, h) in faces:
                        face = gray[y:y+h, x:x+w]
                        resized_face = cv2.resize(face, (100, 100))  
                        known_faces.append(resized_face)
                        known_names.append(os.path.splitext(file_name)[0])
                        print(f"Face found and loaded: {file_name}")
                except Exception as e:
                    print(f"Error loading image {file_name}: {e}")

cap = cv2.VideoCapture(0)

print("Starting webcam for real-time face detection...")
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame from webcam. Exiting...")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face_roi = gray[y:y+h, x:x+w]
        resized_face_roi = cv2.resize(face_roi, (100, 100))  
        recognized = False

        # Bilinen yüzlerle karşılaştır
        for idx, known_face in enumerate(known_faces):
            result = cv2.matchTemplate(resized_face_roi, known_face, cv2.TM_CCOEFF_NORMED)
            (_, max_val, _, _) = cv2.minMaxLoc(result)

            if max_val > 0.6:  
                recognized = True
                name = known_names[idx]
                similarity = round(max_val * 100, 2)  
                cv2.putText(frame, f"{name} ({similarity}%)", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break

        if not recognized:
            cv2.putText(frame, "Face not recognized", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('t'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
