import cv2
import numpy as np

class Buttons:
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.text_scale = 2
        self.text_thick = 2
        self.x_margin = 20
        self.y_margin = 15
        self.buttons = {}
        self.button_index = 0

        self.colors = {"inactive": (200, 200, 200), "active": (0, 255, 0), "border": (0, 0, 255)}
        self.text_colors = {"inactive": (0, 0, 0), "active": (255, 255, 255)}

    def add_button(self, text, x, y):
        textsize = cv2.getTextSize(text, self.font, self.text_scale, self.text_thick)[0]
        right_x = x + (self.x_margin * 2) + textsize[0]
        bottom_y = y + (self.y_margin * 2) + textsize[1]

        self.buttons[self.button_index] = {
            "text": text,
            "position": [x, y, right_x, bottom_y],
            "active": False,
        }
        self.button_index += 1

    def display_buttons(self, frame):
        for b_index, button_value in self.buttons.items():
            button_text = button_value["text"]
            (x, y, right_x, bottom_y) = button_value["position"]
            active = button_value["active"]

            button_color = self.colors["active"] if active else self.colors["inactive"]
            text_color = self.text_colors["active"] if active else self.text_colors["inactive"]
            border_color = self.colors["border"]
            cv2.rectangle(frame, (x, y), (right_x, bottom_y), border_color, 2)  
            cv2.rectangle(frame, (x + 2, y + 2), (right_x - 2, bottom_y - 2), button_color, -1)  

            cv2.putText(frame, button_text, (x + self.x_margin, bottom_y - self.y_margin),
                        self.font, self.text_scale, text_color, self.text_thick)
        return frame

    def button_click(self, mouse_x, mouse_y):
        for b_index, button_value in self.buttons.items():
            (x, y, right_x, bottom_y) = button_value["position"]

            if x <= mouse_x <= right_x and y <= mouse_y <= bottom_y:
                self.buttons[b_index]["active"] = not button_value["active"]

    def active_buttons_list(self):
        return [btn["text"].lower() for btn in self.buttons.values() if btn["active"]]
