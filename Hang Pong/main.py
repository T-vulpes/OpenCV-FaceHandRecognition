import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Genişlik
cap.set(4, 720)   # Yükseklik

def load_image(path, name):
    img = cv2.imread(path)
    if img is None:
        print(f"Hata: {name} yüklenemedi!")
    return img

imgBackground = load_image("images/Background.png", "Background")
imgGameOver = load_image("images/gameOver.png", "Game Over")
imgBall = cv2.imread("images/Ball.png", cv2.IMREAD_UNCHANGED)
imgBat1 = cv2.imread("images/bat1.png", cv2.IMREAD_UNCHANGED)
imgBat2 = cv2.imread("images/bat2.png", cv2.IMREAD_UNCHANGED)

if any(img is None for img in [imgBackground, imgGameOver, imgBall, imgBat1, imgBat2]):
    print("Tüm görsellerin doğru yüklendiğinden emin olun.")
    exit()

detector = HandDetector(detectionCon=0.8, maxHands=2)

ballPos = [100, 100]
speedX, speedY = 15, 15
gameOver = False
score = [0, 0]

while True:
    ret, img = cap.read()
    if not ret:
        print("Kamera görüntüsü alınamadı.")
        break

    img = cv2.flip(img, 1)  # 
    imgRaw = img.copy()
    hands, img = detector.findHands(img, flipType=False)

    # Arka planı ekle
    img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)

    # El ve raket hareketi
    if hands:
        for hand in hands:
            x, y, w, h = hand['bbox']
            h1, w1, _ = imgBat1.shape
            y1 = np.clip(y - h1 // 2, 20, 415)

            if hand['type'] == "Left":  # Sol 
                img = cvzone.overlayPNG(img, imgBat1, (59, y1))
                if 59 < ballPos[0] < 59 + w1 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] += 30
                    score[0] += 1

            if hand['type'] == "Right":  # Sağ 
                img = cvzone.overlayPNG(img, imgBat2, (1195, y1))
                if 1195 - 50 < ballPos[0] < 1195 and y1 < ballPos[1] < y1 + h1:
                    speedX = -speedX
                    ballPos[0] -= 30
                    score[1] += 1

    if ballPos[0] < 40 or ballPos[0] > 1200:
        gameOver = True

    if gameOver:
        img = imgGameOver.copy()
        total_score = f"{score[0]} - {score[1]}"

        cv2.putText(img, f"Total Score: {total_score}", (450, 300), cv2.FONT_HERSHEY_COMPLEX, 1.2, (200, 0, 200), 4)
        if score[0] > score[1]:
            winner = "User1 Wins!"
        elif score[1] > score[0]:
            winner = "User2 Wins!"
        else:
            winner = "It's a Tie!"
        cv2.putText(img, winner, (460, 380), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 255, 0), 4)

    else:
        if ballPos[1] >= 500 or ballPos[1] <= 10:
            speedY = -speedY

        ballPos[0] += speedX
        ballPos[1] += speedY
        img = cvzone.overlayPNG(img, imgBall, ballPos)

        cv2.putText(img, f"User1: {score[0]}", (100, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 4)
        cv2.putText(img, f"User2: {score[1]}", (1000, 50), cv2.FONT_HERSHEY_COMPLEX, 1.5, (0, 0, 0), 4)

    if imgRaw is not None:
        resized_img = cv2.resize(imgRaw, (213, 120))
        img[580:700, 20:233] = resized_img

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord('r'):  # Restart
        ballPos = [100, 100]
        speedX, speedY = 15, 15
        gameOver = False
        score = [0, 0]
    if key == ord('t'):  # cls
        break

cap.release()
cv2.destroyAllWindows()
