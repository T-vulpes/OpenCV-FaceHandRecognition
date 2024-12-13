import cv2
import time

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 10, (frame_width, frame_height))

# Yüz algılama aralığını belirle
detection_interval = 5  # Algılama her 5 karede bir yapılacak
frame_count = 0

while True:
    # Kameradan görüntü al
    check, frame = cap.read()
    if not check:
        break

    # Görüntüyü gri tonlamaya çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüz algılama (her 5 karede bir)
    if frame_count % detection_interval == 0:
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Bulunan yüzleri bulanıklaştır
    for x, y, w, h in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        frame[y:y+h, x:x+w] = cv2.GaussianBlur(frame[y:y+h, x:x+w], (99, 99), 30)

    # Yüz sayısını ekrana yazdır
    cv2.putText(frame, f'Faces Detected: {len(faces)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Videoyu kaydet
    out.write(frame)

    # Görüntüyü göster
    cv2.imshow("Blurface", frame)

    # Çıkış için 't' tuşuna basın
    key = cv2.waitKey(1)
    if key == ord('t'):
        break

    frame_count += 1

# Kaynakları serbest bırak ve pencereleri kapat
cap.release()
out.release()
cv2.destroyAllWindows()
