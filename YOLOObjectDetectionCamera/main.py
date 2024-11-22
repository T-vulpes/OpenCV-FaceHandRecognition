#Real-time object detection using the YOLOv4-tiny model.
#Interactive buttons to toggle detection of specific objects (e.g., person, cell phone, cup).
#Wait a moment for the camera to open.

import cv2
import numpy as np
from gui_buttons import Buttons

button = Buttons()
button.add_button("person", 20, 20)
button.add_button("cell phone", 20, 100)
button.add_button("book", 20, 180)
button.add_button("cup", 20, 260)
button.add_button("remote", 20, 340)

net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1 / 255)

classes = []
with open("classes.txt", "r") as file_object:
    classes = [line.strip() for line in file_object.readlines()]

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
def click_button(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        button.button_click(x, y)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", click_button)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Kamera görüntüsü alınamadı!")
        break

    active_buttons = button.active_buttons_list()
    (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.4, nmsThreshold=0.4)

    for class_id, score, bbox in zip(class_ids, scores, bboxes):
        class_name = classes[int(class_id)]
        (x, y, w, h) = bbox
        if class_name in active_buttons:
            cv2.putText(frame, f"{class_name}: {int(score * 100)}%", (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    button.display_buttons(frame)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
