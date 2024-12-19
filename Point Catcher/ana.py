# Wait for the camera to open.
# Point to the point with your index finger...

import cv2
import mediapipe as mp
import random
import time
import cvzone

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

cx, cy = random.randint(100, 1100), random.randint(100, 600)
score = 0
timeStart = time.time()
totalTime = 30
circle_color = (128, 0, 128)  
text_color = (128, 0, 128)    

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_img)

    if time.time() - timeStart < totalTime:
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                index_finger_tip = hand_landmarks.landmark[8]
                h, w, _ = img.shape
                index_x, index_y = int(index_finger_tip.x * w), int(index_finger_tip.y * h)
                dist = ((index_x - cx) ** 2 + (index_y - cy) ** 2) ** 0.5
                if dist < 30:  
                    score += 1
                    cx, cy = random.randint(100, 1100), random.randint(100, 600)  
                    circle_color = (0, 255, 0) 
                    break
                else:
                    circle_color = (128, 0, 128) 

        cv2.circle(img, (cx, cy), 30, circle_color, cv2.FILLED)
        cv2.circle(img, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), 20, (255, 255, 255), 2)
        cv2.circle(img, (cx, cy), 30, (50, 50, 50), 2)

        cvzone.putTextRect(img, f'Time: {int(totalTime - (time.time() - timeStart))}', (1000, 75), 
                           scale=3, offset=20, colorR=text_color)
        cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (60, 75), 
                           scale=3, offset=20, colorR=text_color)
    else:
        cvzone.putTextRect(img, 'Game Over', (400, 400), scale=5, offset=30, thickness=7, colorR=text_color)
        cvzone.putTextRect(img, f'Your Score: {score}', (450, 500), scale=3, offset=20, colorR=text_color)
        cvzone.putTextRect(img, 'Press R to restart', (460, 575), scale=2, offset=10, colorR=text_color)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        timeStart = time.time()
        score = 0

    if key == 84:  # T
        break

cap.release()
cv2.destroyAllWindows()
