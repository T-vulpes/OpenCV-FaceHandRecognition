#!Wait 1-2 minutes for the image to appear on the screen.!
# The project tracks the tips of your thumb and index finger.
#   - Increase Volume: Move your thumb and index finger farther apart.
#   - Decrease Volume: Bring your thumb and index finger closer together.

import cv2
import time
import numpy as np
import modelfin as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL 
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wcam, hcam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wcam) 
cap.set(4, hcam)  
pTime = 0

detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers() 
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volRange = volume.GetVolumeRange()
minVol = volRange[0]  
maxVol = volRange[1]  

volBar = 400
volPer = 0

while True:
    success, img = cap.read() 
    
    if not success:
        print("Cannot get image from camera!")
        continue

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    
    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [50, 300], [minVol, maxVol])  
        volBar = np.interp(length, [50, 300], [400, 150])  
        volPer = np.interp(length, [50, 300], [0, 100])  

        volume.SetMasterVolumeLevel(vol, None)

        if length < 50:
            cv2.circle(img, ((x1 + x2) // 2, (y1 + y2) // 2), 15, (0, 255, 0), cv2.FILLED)
        
        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
