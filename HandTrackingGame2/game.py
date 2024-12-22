# I saw the original content of this file on the 'Iknowpython' YouTube channel,
#        and I decided to upload it with 1-2 changes, including the addition of a custom sound effect.

import cv2
import mediapipe as mp
import random
import time
import  pygame


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def play_success_sound():
    pygame.mixer.init()  
    pygame.mixer.music.load("success.mp3")  
    pygame.mixer.music.play()  

def reset_game():
    global score, enemy_x, enemy_y, start_time
    score = 0
    enemy_x = random.randint(50, 600)
    enemy_y = random.randint(50, 400)
    start_time = time.time()

def draw_enemy(img):
    cv2.circle(img, (enemy_x, enemy_y), 25, (0, 200, 0), 5)

# Çarpışma kontrolü fonksiyonu
def check_collision(index_x, index_y):
    """İşaret parmağı ile düşman arasında çarpışma kontrolü."""
    global score, enemy_x, enemy_y
    if enemy_x - 25 < index_x < enemy_x + 25 and enemy_y - 25 < index_y < enemy_y + 25:
        score += 1
        play_success_sound()
        enemy_x = random.randint(50, 600)
        enemy_y = random.randint(50, 400)

# Kamera başlatma
cap = cv2.VideoCapture(0)

# İlk oyun ayarlarını başlat
reset_game()
time_limit = 30  # Oyun süresi (saniye)

while True:
    with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Görüntüyü çevir ve RGB'ye dönüştür
            frame = cv2.flip(frame, 1)
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Mediapipe ile işleme
            results = hands.process(img_rgb)
            
            # Görüntüyü tekrar BGR formatına çevir
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

            # Skoru yazdır
            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (255, 0, 255)
            cv2.putText(img_bgr, f"Score: {score}", (10, 50), font, 1, color, 2, cv2.LINE_AA)

            # Kalan süreyi yazdır
            elapsed_time = time.time() - start_time
            remaining_time = max(0, int(time_limit - elapsed_time))
            cv2.putText(img_bgr, f"Time: {remaining_time}s", (10, 100), font, 1, color, 2, cv2.LINE_AA)

            # Düşmanı çiz
            draw_enemy(img_bgr)

            # El tespiti ve işaret parmağı koordinatları
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(img_bgr, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    # İşaret parmağı ucu koordinatları
                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    h, w, _ = img_bgr.shape
                    index_x = int(index_finger_tip.x * w)
                    index_y = int(index_finger_tip.y * h)

                    # Parmağı düşman gibi bir daire ile işaretle
                    cv2.circle(img_bgr, (index_x, index_y), 25, (0, 200, 0), 5)

                    # Çarpışma kontrolü
                    check_collision(index_x, index_y)

            cv2.imshow("Hand Tracking Game", img_bgr)

            if remaining_time <= 0:
                cv2.putText(img_bgr, "Time's Up! Press X to Restart", (50, 300), font, 1, (0, 0, 255), 3, cv2.LINE_AA)
                cv2.imshow("Hand Tracking Game", img_bgr)
                if cv2.waitKey(0) & 0xFF == ord('x'):  
                    reset_game()
                    break
                else:
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

            if cv2.waitKey(1) & 0xFF == ord('t'):
                cap.release()
                cv2.destroyAllWindows()
                exit()
