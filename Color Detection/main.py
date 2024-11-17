import cv2
import numpy as np
import json

PROJECT_NAME = "Color Detection and Tracking Tool"

def nothing(x):
    pass

def save_settings(settings_file, settings):
    with open(settings_file, "w") as file:
        json.dump(settings, file)

def load_settings(settings_file):
    try:
        with open(settings_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Kamera bağlantısı başarısız!")
    exit()

cv2.namedWindow("Trackbars")
settings_file = "trackbar_settings.json"

loaded_settings = load_settings(settings_file)

cv2.createTrackbar("L-H", "Trackbars", loaded_settings.get("L-H", 0) if loaded_settings else 0, 179, nothing)
cv2.createTrackbar("L-S", "Trackbars", loaded_settings.get("L-S", 0) if loaded_settings else 0, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", loaded_settings.get("L-V", 0) if loaded_settings else 0, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", loaded_settings.get("U-H", 179) if loaded_settings else 179, 179, nothing)
cv2.createTrackbar("U-S", "Trackbars", loaded_settings.get("U-S", 255) if loaded_settings else 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", loaded_settings.get("U-V", 255) if loaded_settings else 255, 255, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera çerçevesi alınamadı!")
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Trackbar değerlerini alma
    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    u_h = cv2.getTrackbarPos("U-H", "Trackbars")
    u_s = cv2.getTrackbarPos("U-S", "Trackbars")
    u_v = cv2.getTrackbarPos("U-V", "Trackbars")

    lower_color = np.array([l_h, l_s, l_v])
    upper_color = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_color, upper_color)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel, iterations=1)
    mask = cv2.dilate(mask, kernel, iterations=1)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 500:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    cv2.imshow("Result", result)

    key = cv2.waitKey(1)
    if key == 27:  
        break
    elif key == ord('s'):  
        current_settings = {
            "L-H": l_h, "L-S": l_s, "L-V": l_v,
            "U-H": u_h, "U-S": u_s, "U-V": u_v
        }
        save_settings(settings_file, current_settings)
        print("Ayarlar kaydedildi!")

cap.release()
cv2.destroyAllWindows()
