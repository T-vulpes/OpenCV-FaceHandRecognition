import cv2
import pyautogui

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
cam = cv2.VideoCapture(0)

screen_width, screen_height = pyautogui.size()
previous_mouse_x, previous_mouse_y = 0, 0

THRESHOLD = 15
while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h // 2, x:x + w]
        roi_color = frame[y:y + h // 2, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=4)
        for (ex, ey, ew, eh) in eyes:
            # Gözün merkezi
            eye_center_x = x + ex + ew // 2
            eye_center_y = y + ey + eh // 2

            mouse_x = int(screen_width / frame.shape[1] * eye_center_x)
            mouse_y = int(screen_height / frame.shape[0] * eye_center_y)

            smooth_x = int(0.7 * previous_mouse_x + 0.3 * mouse_x)
            smooth_y = int(0.7 * previous_mouse_y + 0.3 * mouse_y)

            if abs(smooth_x - previous_mouse_x) > THRESHOLD or abs(smooth_y - previous_mouse_y) > THRESHOLD:
                pyautogui.moveTo(smooth_x, smooth_y, duration=0.1)

            previous_mouse_x, previous_mouse_y = smooth_x, smooth_y
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 2)

    cv2.imshow("Eye-Controlled Cursor", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
