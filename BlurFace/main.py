import cv2
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (frame_width, frame_height))

detection_interval = 5  
frame_count = 0

while True:
    check, frame = cap.read()
    if not check:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if frame_count % detection_interval == 0:
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for x, y, w, h in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        frame[y:y+h, x:x+w] = cv2.GaussianBlur(frame[y:y+h, x:x+w], (99, 99), 30)

    cv2.putText(frame, f'Faces Detected: {len(faces)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    out.write(frame)
    cv2.imshow("Blurface", frame)

    key = cv2.waitKey(1)
    if key == ord('t'):
        break
    frame_count += 1

cap.release()
out.release()
cv2.destroyAllWindows()
