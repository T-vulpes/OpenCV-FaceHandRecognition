import cv2
import numpy as np

cap = cv2.VideoCapture("eye_recording.flv")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    roi = frame[269:795, 537:1416]
    rows, cols, _ = roi.shape
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)

    _, threshold = cv2.threshold(gray_roi, 3, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        if x < 350:
            cv2.putText(roi, "Looking left", (200, 100), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 0), 2, cv2.LINE_AA)
        elif x > 500:
            cv2.putText(roi, "Looking right", (200, 100), cv2.FONT_HERSHEY_COMPLEX, 1.5, (255, 255, 0), 2, cv2.LINE_AA)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.line(roi, (x + int(w / 2), 0), (x + int(w / 2), rows), (0, 255, 0), 2)
        cv2.line(roi, (0, y + int(h / 2)), (cols, y + int(h / 2)), (0, 255, 0), 2)
        break

    cv2.imshow("Threshold", threshold)
    cv2.imshow("Gray ROI", gray_roi)
    cv2.imshow("ROI", roi)

    key = cv2.waitKey(30)
    if key == 27:  #  ESC
        break

cv2.destroyAllWindows()
