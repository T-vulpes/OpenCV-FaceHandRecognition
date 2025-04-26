#Wait for the camera to open...
import cv2
import time
import winsound

cam = cv2.VideoCapture(0)

while True:
    _, im = cam.read()
    _, im2 = cam.read()

    absdiff = cv2.absdiff(im, im2)
    gray = cv2.cvtColor(absdiff, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for x in contours:
        if cv2.contourArea(x) < 5000:
            continue
        winsound.Beep(500, 100)

    cv2.imshow("Camera", thresh)
    if cv2.waitKey(10) == ord('t'):  # 'T'
        break

cam.release()
cv2.destroyAllWindows()
