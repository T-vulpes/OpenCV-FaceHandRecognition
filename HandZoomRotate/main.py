#Подождите, пока камера включится.

import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

cx, cy = 500, 500
scale = 0
angle = 0
startDist = None
startAngle = None

detector = HandDetector(detectionCon=0.8)
image = cv2.imread("image.jpg")

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img)

    if len(hands) == 2:
        lmList1 = hands[0]["lmList"] 
        lmList2 = hands[1]["lmList"]  

        point1 = lmList1[8][:2]  
        point2 = lmList2[8][:2]  

        if startDist is None:
            length, info, img = detector.findDistance(point1, point2, img)
            startDist = length
            startAngle = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])

        length, info, img = detector.findDistance(point1, point2, img)
        currentAngle = np.arctan2(point2[1] - point1[1], point2[0] - point1[0])

        # Calculate scale and rotation angle
        scale = int((length - startDist) // 2)
        angle = int(np.degrees(currentAngle - startAngle))

        # Update position based on midpoint
        cx, cy = info[4:]
    else:
        startDist = None
        startAngle = None

    # Resize and rotate the image
    h1, w1, _ = image.shape
    newH, newW = max(((h1 + scale) // 2) * 2, 1), max(((w1 + scale) // 2) * 2, 1)
    resized_image = cv2.resize(image, (newW, newH))
    
    # Rotation matrix
    M = cv2.getRotationMatrix2D((newW // 2, newH // 2), angle, 1)
    rotated_image = cv2.warpAffine(resized_image, M, (newW, newH))

    try:
        img[cy - newH // 2:cy + newH // 2, cx - newW // 2:cx + newW // 2] = rotated_image
    except ValueError:
        pass

    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('t'):
        break

cap.release()
cv2.destroyAllWindows()
