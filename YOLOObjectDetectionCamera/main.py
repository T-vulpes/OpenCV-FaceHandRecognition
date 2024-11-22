import cv2
import numpy as np
from gui_buttons import Buttons

# Buttons instance
button = Buttons()
button.add_button("person", 20, 20)
button.add_button("cell phone", 20, 100)
button.add_button("book", 20, 180)
button.add_button("cup", 20, 260)
button.add_button("remote", 20, 340)

# Load YOLO model
net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1 / 255)

# Load classes
classes = []
with open("classes.txt", "r") as file_object:
    classes = [line.strip() for line in file_object.readlines()]

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Mouse callback
def click_button(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        button.button_click(x, y)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_button)

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera görüntüsü alınamadı!")
        break

    # Get active buttons
    active_buttons = button.active_buttons_list()

    # Detect objects
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.4, nmsThreshold=0.4)

    # Draw bounding boxes for active buttons
    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        class_name = classes[int(class_id)]
        (x, y, w, h) = bbox

        # Only draw boxes for active buttons
        if class_name in active_buttons:
            cv2.putText(frame, f"{class_name}: {int(score * 100)}%", (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Display buttons
    button.display_buttons(frame)

    # Show frame
    cv2.imshow("Frame", frame)

    # Exit on ESC key
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
