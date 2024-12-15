import cv2
import time
import mediapipe as mp
import serial

arduino = serial.Serial(port='COM6', baudrate=9600, timeout=0.1)  # Timeout küçük olmalı
time.sleep(2)  

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

prev_x = None
movement = ""
last_command_time = 0  
command_interval = 0.5 

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Kamera görüntüsü alınamadı.")
            continue

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                x_coord = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                current_time = time.time()  # Şu anki zamanı al
                if prev_x is not None:
                    if x_coord - prev_x > 0.05 and (current_time - last_command_time > command_interval):  # Sağ hareket
                        movement = "Sağ"
                        try:
                            arduino.write(b"RIGHT\n")  
                        except serial.SerialException as e:
                            print(f"Seri bağlantı hatası: {e}")
                        last_command_time = current_time  
                    elif prev_x - x_coord > 0.05 and (current_time - last_command_time > command_interval):  # Sol hareket
                        movement = "Sol"
                        try:
                            arduino.write(b"LEFT\n")  
                        except serial.SerialException as e:
                            print(f"Seri bağlantı hatası: {e}")
                        last_command_time = current_time  # Zamanı güncelle

                # Önceki x değerini güncelle
                prev_x = x_coord

                # Metni görüntüye ekle
                cv2.putText(image, movement, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

                # El işaretlerini çiz
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2))

        # Görüntüyü göster
        cv2.imshow('El Hareket Algılama', image)

        # Çıkış için ESC tuşu
        if cv2.waitKey(5) & 0xFF == 27:
            break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
arduino.close()
