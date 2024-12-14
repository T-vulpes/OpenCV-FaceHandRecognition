import cv2
import cvzone
import os
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import time

video = cv2.VideoCapture(0)
video.set(3, 640)  # Genişlik
video.set(4, 480)  # Yükseklik
sgmnt = SelfiSegmentation()
prev_time = 0

imgbg = cv2.imread("2.jpg")  # Arka plan görseli
if imgbg is not None:
    imgbg = cv2.resize(imgbg, (640, 480))  # Kameranın çözünürlüğüne yeniden boyutlandır
else:
    print("Arka plan görseli yüklenemedi.")
    exit()

while True:
    success, img = video.read()  # Kameradan görüntü alınıyor
    if not success:
        print("Kamera görüntüsü alınamadı.")
        break
    
    # Arka planı kaldırma
    imgout = sgmnt.removeBG(img, imgbg)  # threshold parametresi kaldırıldı
    
    # Görüntüleri yan yana yerleştirme
    imgstack = cvzone.stackImages([img, imgout], 2, 1)
    
    # FPS hesaplama
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    
    # FPS'yi üzerine yazma
    cv2.putText(imgstack, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    # Görüntüleri ekranda gösterme
    #cv2.imshow("Original Image", img)
    #cv2.imshow("Processed Image", imgout)
    cv2.imshow("Image Stack", imgstack)

    # Çıkış için 'q' tuşuna basılabilir
    if cv2.waitKey(1) & 0xFF == ord('t'):
        break

# Kaynakları serbest bırak ve pencereleri kapat
video.release()
cv2.destroyAllWindows()
