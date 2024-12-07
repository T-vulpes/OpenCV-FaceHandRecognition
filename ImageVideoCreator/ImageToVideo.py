import cv2
import os

path = "img/"
pre_img = os.listdir(path)  # Klasördeki tüm dosyaları listele

# Sadece desteklenen resim formatlarını seç
supported_formats = ['.jpg', '.png', '.jpeg', '.bmp']
img_paths = [os.path.join(path, f) for f in pre_img if os.path.splitext(f)[1].lower() in supported_formats]

if not img_paths:
    raise ValueError("Klasörde geçerli resim dosyası bulunamadı. Lütfen 'img/' klasörünü kontrol edin.")

frame = cv2.imread(img_paths[0])
if frame is None:
    raise ValueError("İlk görüntü yüklenemedi. Lütfen resim dosyalarının bozuk olmadığından emin olun.")

height, width, layers = frame.shape
size = (width, height)

cv2_fourcc = cv2.VideoWriter_fourcc(*'XVID')  # Alternatif codec: 'mp4v', 'DIVX'
media = cv2.VideoWriter("newvideo.mp4", cv2_fourcc, 4, size)  # 24=fps

for image_path in img_paths:
    frame = cv2.imread(image_path)
    if frame is None:
        print(f"Dosya yüklenemedi: {image_path}")
        continue

    if frame.shape[:2] != (height, width):
        frame = cv2.resize(frame, size)

    media.write(frame)

media.release()
print("Yeni video başarıyla kaydedildi!")
