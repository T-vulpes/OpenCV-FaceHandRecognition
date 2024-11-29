import cv2

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("frame")

cv2.createTrackbar("test", "frame", 50, 500, nothing)
cv2.createTrackbar("color/gray", "frame", 0, 1, nothing)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera image could not be obtained.")
        break

    test = cv2.getTrackbarPos("test", "frame")
    font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX  
    text_color = (255, 0, 0)  
    cv2.putText(frame, f"Value: {test}", (50, 150), font, 2, text_color, 3)

    color_gray = cv2.getTrackbarPos("color/gray", "frame")
    if color_gray == 1:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key == 27:  
        break

cap.release()
cv2.destroyAllWindows()
