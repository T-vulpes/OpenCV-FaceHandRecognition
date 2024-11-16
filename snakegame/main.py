#Please wait for the video to open.

import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = [] 
        self.lengths = []  
        self.currentLength = 0  
        self.allowedLength = 150  
        self.previousHead = 0, 0  

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.imgFood = cv2.resize(self.imgFood, (70, 70))  
        self.hFood, self.wFood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()
        self.score = 0
        self.gameOver = False

    def randomFoodLocation(self):
        self.foodPoint = random.randint(300, 1000), random.randint(100, 500)

    def update(self, imgMain, currentHead):
        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400],scale=7, thickness=5, offset=20)
            cvzone.putTextRect(imgMain, f'Your Score: {self.score}', [300, 550],scale=7, thickness=5, offset=20)
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            rx, ry = self.foodPoint
            if rx - self.wFood // 2 < cx < rx + self.wFood // 2 and \
                    ry - self.hFood // 2 < cy < ry + self.hFood // 2:
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1

            for i in range(len(self.points) - 1):
                r = int((255 / len(self.points)) * i)
                g = int((128 / len(self.points)) * (len(self.points) - i))
                b = 0
                cv2.line(imgMain, self.points[i], self.points[i + 1], (r, g, b), 20)

            if self.points:
                cv2.circle(imgMain, self.points[-1], 20, (0, 255, 255), cv2.FILLED) 

            imgMain = cvzone.overlayPNG(imgMain, self.imgFood,(rx - self.wFood // 2, ry - self.hFood // 2))

            cvzone.putTextRect(imgMain, f'Score: {self.score}', [50, 80],scale=3, thickness=3, offset=10)

            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0, 255, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx, cy), True)

            if -1 <= minDist <= 1:
                self.gameOver = True
                self.points = []  
                self.lengths = []  
                self.currentLength = 0  
                self.allowedLength = 150  
                self.previousHead = 0, 0  
                self.randomFoodLocation()

        return imgMain

game = SnakeGameClass("apple.png")
game_started = False  

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)

    if not game_started:
        start_button_x, start_button_y, button_w, button_h = 100, 100, 150, 75
        cv2.rectangle(img, (start_button_x, start_button_y), 
                      (start_button_x + button_w, start_button_y + button_h), 
                      (0, 255, 0), cv2.FILLED)
        cv2.putText(img, "Start", (start_button_x + 20, start_button_y + 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 4)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]  # İşaret parmağı koordinatları
        x, y = pointIndex

        if not game_started and start_button_x < x < start_button_x + button_w and start_button_y < y < start_button_y + button_h:
            game_started = True

        if game_started:
            img = game.update(img, pointIndex)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
        game_started = False
        game.score = 0

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
