#Wait a moment for the camera to open.

import cv2
import mediapipe as mp
import random
import time
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

cap = cv2.VideoCapture(0)

start_button_coords = (50, 50, 250, 130)  
game_active = False
countdown_start = None
user_choice = None
computer_choice = None
result_text = ""
show_computer_choice = False  

rock_img = cv2.imread('images/rock.png')
paper_img = cv2.imread('images/paper.png')
scissors_img = cv2.imread('images/scissors.png')

def draw_gradient_button(frame, coords, color1, color2, text):
    x1, y1, x2, y2 = coords
    button_width = x2 - x1
    button_height = y2 - y1

    button = np.zeros((button_height, button_width, 3), dtype=np.uint8)
    for i in range(button_width):
        color_ratio = i / button_width
        r = int(color1[0] * (1 - color_ratio) + color2[0] * color_ratio)
        g = int(color1[1] * (1 - color_ratio) + color2[1] * color_ratio)
        b = int(color1[2] * (1 - color_ratio) + color2[2] * color_ratio)
        button[:, i] = (b, g, r)

    mask = np.zeros_like(button, dtype=np.uint8)
    radius = min(button_height, button_width) // 2
    cv2.rectangle(mask, (radius, 0), (button_width - radius, button_height), (255, 255, 255), -1)
    cv2.circle(mask, (radius, radius), radius, (255, 255, 255), -1)
    cv2.circle(mask, (button_width - radius, radius), radius, (255, 255, 255), -1)
    button = cv2.bitwise_and(button, mask)

    frame[y1:y2, x1:x2] = cv2.addWeighted(frame[y1:y2, x1:x2], 0.5, button, 0.5, 0)
    text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = x1 + (button_width - text_size[0]) // 2
    text_y = y1 + (button_height + text_size[1]) // 2
    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

def determine_hand_shape(landmarks):
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    if (thumb_tip.y > landmarks[3].y and
        index_tip.y > landmarks[6].y and
        middle_tip.y > landmarks[10].y and
        ring_tip.y > landmarks[14].y and
        pinky_tip.y > landmarks[18].y):
        return "Rock"

    if (thumb_tip.y < landmarks[3].y and
        index_tip.y < landmarks[6].y and
        middle_tip.y < landmarks[10].y and
        ring_tip.y < landmarks[14].y and
        pinky_tip.y < landmarks[18].y):
        return "Paper"

    if (index_tip.y < landmarks[6].y and
        middle_tip.y < landmarks[10].y and
        ring_tip.y > landmarks[14].y and
        pinky_tip.y > landmarks[18].y):
        return "Scissors"

    return "Undefined"

def draw_computer_choice(frame, choice):
    h, w, _ = frame.shape
    choice_img = None
    if choice == "Rock":
        choice_img = rock_img
    elif choice == "Paper":
        choice_img = paper_img
    elif choice == "Scissors":
        choice_img = scissors_img

    if choice_img is not None:
        resized_img = cv2.resize(choice_img, (150, 150))
        y_offset, x_offset = 10, w - 160
        frame[y_offset:y_offset+150, x_offset:x_offset+150] = resized_img
        cv2.putText(frame, f"Computer: {choice}", (w - 320, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

def determine_winner(user, computer):
    """ Oyunun sonucunu belirle. """
    if user == computer:
        return "It's a Tie!"
    elif (user == "Rock" and computer == "Scissors") or \
         (user == "Paper" and computer == "Rock") or \
         (user == "Scissors" and computer == "Paper"):
        return "User Wins!"
    else:
        return "Computer Wins!"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)
    draw_gradient_button(frame, start_button_coords, (138, 43, 226), (30, 144, 255), "START")

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x, y = int(hand_landmarks.landmark[9].x * frame.shape[1]), int(hand_landmarks.landmark[9].y * frame.shape[0])
            if (start_button_coords[0] < x < start_button_coords[2] and
                start_button_coords[1] < y < start_button_coords[3]):
                if not game_active:
                    game_active = True
                    countdown_start = time.time()
                    computer_choice = random.choice(["Rock", "Paper", "Scissors"])
                    show_computer_choice = False  

            # Kull
            if game_active and countdown_start:
                elapsed = time.time() - countdown_start
                if elapsed < 3:  
                    cv2.putText(frame, str(3 - int(elapsed)), (250, 250), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 10)
                elif elapsed >= 3: 
                    user_choice = determine_hand_shape(hand_landmarks.landmark)
                    result_text = determine_winner(user_choice, computer_choice)
                    game_active = False
                    show_computer_choice = True  # 

    if user_choice:
        cv2.putText(frame, f"User: {user_choice}", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if show_computer_choice:
        draw_computer_choice(frame, computer_choice)
        cv2.putText(frame, result_text, (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Rock-Paper-Scissors", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
