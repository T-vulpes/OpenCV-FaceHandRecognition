import cv2

cap = cv2.VideoCapture("videoplayback.mp4")

timer = 10000

while True:
    success, img = cap.read()
    
    # Eğer başarıyla görüntü alınamazsa döngüden çık
    if not success:
        print("Video sona erdi veya görüntü alınamadı.")
        break
    
    outfile = 'output/img_%s.jpg' % (timer)
    timer += 1
    print(outfile)
    
    # Görüntüyü kaydet
    cv2.imwrite(outfile, img)
    
    # Görüntüyü göster
    cv2.imshow("Image", img)
    
    # Döngüyü durdurmak için 'q' tuşuna basabilirsiniz
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
