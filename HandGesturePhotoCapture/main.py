import cv2
import mediapipe as mp
import time
from playsound import playsound

# Mediapipe Hand Detection
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
countdown_start = 0
countdown_active = False
hand_shown_once = False  # Elin bir kez gösterilip gösterilmediğini takip eder

while True:
    ret, img = cap.read()
    if not ret:
        break
    
    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Hand detection
    result = hands.process(rgb)
    hand_detected = False
    
    if result.multi_hand_landmarks:
        hand_detected = True
        hand_shown_once = True  # El bir kez gösterildi
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    
    # Başlama koşulu: El bir kez gösterildiyse ve sonra kaybolduysa
    if hand_shown_once and not hand_detected:
        if not countdown_active:
            countdown_start = time.time()
            countdown_active = True

    # Countdown logic
    if countdown_active:
        elapsed = time.time() - countdown_start
        countdown = int(3 - elapsed)
        
        if countdown > 0:
            cv2.putText(img, f"Photo in {countdown}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        else:
            cv2.imwrite("selfie.jpg", img)
            playsound("effect.mp3")
            countdown_active = False
            hand_shown_once = False  # Tekrar işlem yapılması için resetlenir

    # Display the image
    cv2.imshow("Hand Detection", img)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key to exit
        break

cap.release()
cv2.destroyAllWindows()