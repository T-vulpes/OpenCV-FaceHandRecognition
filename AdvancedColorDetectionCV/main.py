#Wait a moment for the camera to turn on.

import cv2
import numpy as np
from tkinter import Tk, Button

def get_limits(color):
    color_ranges = {
        "yellow": ([20, 100, 100], [30, 255, 255]),
        "red": ([0, 120, 70], [10, 255, 255]),
        "green": ([40, 40, 40], [70, 255, 255]),
        "blue": ([100, 150, 0], [140, 255, 255]),
        "black": ([0, 0, 0], [180, 255, 50]),
        "orange": ([10, 100, 100], [25, 255, 255]),
        "purple": ([140, 100, 100], [160, 255, 255]),
        "gray": ([0, 0, 50], [180, 50, 200]),
        "white": ([0, 0, 200], [180, 20, 255]),
    }

    lower, upper = color_ranges[color]
    return np.array(lower, dtype=np.uint8), np.array(upper, dtype=np.uint8)

def process_frame(color_name, colors, frame, image_hsv):
    bgr_value = colors[color_name]
    lower_limit, upper_limit = get_limits(color=color_name)
    mask = cv2.inRange(image_hsv, lower_limit, upper_limit)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        if cv2.contourArea(contour) > 500: 
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), bgr_value, 2)
            cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, bgr_value, 2)

    return frame

colors = {
    "yellow": (0, 255, 255),
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "black": (0, 0, 0),
    "orange": (0, 165, 255),
    "purple": (128, 0, 128),
    "gray": (128, 128, 128),
    "white": (255, 255, 255),
}
selected_color = ["yellow"]

def set_color(color_name):
    selected_color[0] = color_name

root = Tk()
root.title("Renk Seçici")

for color_name in colors.keys():
    btn = Button(root, text=color_name, bg=color_name, command=lambda c=color_name: set_color(c))
    btn.pack(fill="x")

video = cv2.VideoCapture(0)

def video_loop():
    ret, frame = video.read()
    if not ret:
        root.quit()
        return

    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame = process_frame(selected_color[0], colors, frame, image_hsv)
    cv2.imshow("CAMERA", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('t'):
        root.quit()
        return
    root.after(10, video_loop)

root.after(0, video_loop)
root.mainloop()
video.release()
cv2.destroyAllWindows()
