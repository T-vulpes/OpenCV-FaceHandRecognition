import cv2

cap = cv2.VideoCapture("newvideo.mp4")

cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
success, img = cap.read()

if not success:
    raise ValueError("Video okunamadı. Dosya yolunu kontrol edin veya video bozuk olabilir.")

size = (img.shape[1], img.shape[0])  
video = cv2.VideoWriter("fasternewvideo.mp4", cv2_fourcc, 30, size)  # Output video adı, fourcc, fps, size

while success:
    video.write(img)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('t'):
        break

    success, img = cap.read()  

# st bırak
cap.release()
video.release()
cv2.destroyAllWindows()

print("Yeni video başarıyla kaydedildi: fasternewvideo.mp4")
