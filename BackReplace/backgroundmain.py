#Wait a moment for the camera to open......<3
import cv2
import cvzone
import os
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import time

video = cv2.VideoCapture(0)
video.set(3, 640)  
video.set(4, 480)  
sgmnt = SelfiSegmentation()
prev_time = 0

imgbg = cv2.imread("2.jpg")  
if imgbg is not None:
    imgbg = cv2.resize(imgbg, (640, 480))  
else:
    print("Background image could not be loaded.")
    exit()

while True:
    success, img = video.read()  
    if not success:
        print("Camera image could not be obtained.")
        break
    
    imgout = sgmnt.removeBG(img, imgbg)  
    imgstack = cvzone.stackImages([img, imgout], 2, 1)
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time
    
    cv2.putText(imgstack, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    #cv2.imshow("Original Image", img)
    #cv2.imshow("Processed Image", imgout)
    cv2.imshow("Image Stack", imgstack)

    if cv2.waitKey(1) & 0xFF == ord('t'):
        break

video.release()
cv2.destroyAllWindows()
