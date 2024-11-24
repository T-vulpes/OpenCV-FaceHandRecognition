 #  - If the hand is open, it sends a `1` to turn the LED ON.
 #  - If the hand is closed, it sends a `0` to turn the LED OFF.
 #  - Wait a moment for the camera to open.

import cv2
import mediapipe as mp
import serial
import time

arduino = serial.Serial(port='COM6', baudrate=9600, timeout=.1)  
time.sleep(2)  
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        x, y = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
        x1, y1 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y

        font = cv2.FONT_HERSHEY_PLAIN
        if y1 > y:
            cv2.putText(image, "KAPALI", (10, 50), font, 4, (0, 0, 0), 3)
            arduino.write(b'0')  # Arduino'ya '0' gönder (LED kapalı)
        else:
            cv2.putText(image, "ACIK", (10, 50), font, 4, (0, 0, 0), 3)
            arduino.write(b'1')  # Arduino'ya '1' gönder (LED açık)
        
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
arduino.close()
