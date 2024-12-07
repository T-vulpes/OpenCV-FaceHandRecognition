import cv2

cap = cv2.VideoCapture("newvideo.mp4")
cv2_fourcc = cv2.VideoWriter_fourcc(*'mp4v')
success, img = cap.read()

if not success:
    raise ValueError("The video could not be read. Check the file path or the video may be corrupt.")

size = (img.shape[1], img.shape[0])  
video = cv2.VideoWriter("fasternewvideo.mp4", cv2_fourcc, 30, size)  

while success:
    video.write(img)
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('t'):
        break

    success, img = cap.read()  

cap.release()
video.release()
cv2.destroyAllWindows()

print("New video saved successfully: fasternewvideo.mp4")
