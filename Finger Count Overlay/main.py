import cv2
import time
import os
import HandtrackingModule as htm

WCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, WCam)
cap.set(4, hCam)

folderPath = "images/"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(len(overlayList))

ptime = 0
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        finger = []

        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            finger.append(1)
        else:
            finger.append(0)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                finger.append(1)
            else:
                finger.append(0)

        print(finger)
        totalfinger = finger.count(1)

        overlay = overlayList[totalfinger - 1]
        resized_overlay = cv2.resize(overlay, (150, 150))  

        h, w, c = resized_overlay.shape
        img[0:h, 0:w] = resized_overlay

        cv2.rectangle(img, (20, 225), (110, 290), (0, 0, 0), cv2.FILLED)  # Adjusted width
        cv2.putText(img, str(totalfinger), (50, 280), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)  # Smaller font

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime
    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)

    # Check for 't' key press
    if cv2.waitKey(1) & 0xFF == ord('t'):
        print("Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
