import cv2
from cvzone.HandTrackingModule import HandDetector
import cvzone
import csv
import threading
import time

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  
cap.set(4, 720)   

detector = HandDetector(detectionCon=0.7, maxHands=1)  
pathcsv = "quiz.csv"

with open(pathcsv, newline='', encoding="iso-8859-9") as f:
    reader = csv.reader(f, delimiter=';')
    dataquiz = [row for row in reader][1:]

class QuizQuestion:
    def __init__(self, data):
        self.question = data[0]
        self.choice1 = data[1]
        self.choice2 = data[2]
        self.choice3 = data[3]
        self.choice4 = data[4]
        self.answer = data[5]
        self.useransw = None
        self.answered = False
        self.color_boxes = [(0, 0, 0)] * 4  

    def update(self, cursor, bboxs):
        for x, bbox in enumerate(bboxs):
            x1, y1, x2, y2 = bbox
            if x1 < cursor[0] < x2 and y1 < cursor[1] < y2:
                self.useransw = x + 1  # Kullanıcının seçtiği şık
                self.answered = True
                self.apply_colors()  # Renkleri uygula
                return True
        return False

    def apply_colors(self):
        """
        Şık kutularına doğru/yanlış renklerini uygular.
        """
        self.color_boxes = [(0, 0, 0)] * 4  # Tüm kutuları siyaha döndür
        if self.answered:
            correct_index = self.get_answer_index() - 1
            if self.useransw == correct_index + 1:
                self.color_boxes[correct_index] = (0, 255, 0)  # Doğru şık: Yeşil
            else:
                self.color_boxes[self.useransw - 1] = (0, 0, 255)  # Yanlış şık: Kırmızı
                self.color_boxes[correct_index] = (0, 255, 0)  # Doğru şık: Yeşil

    def get_answer_index(self):
        """
        Doğru cevabın indeksini döndürür.
        """
        return {"A": 1, "B": 2, "C": 3, "D": 4}[self.answer]


quiz_list = [QuizQuestion(row) for row in dataquiz if len(row) == 6]
qno = 0
qtotal = len(quiz_list)
score = 0
running = True
lock = threading.Lock()

# Global değişkenler
frame = None
current_hand = None

# Kamera okuma thread'i
def capture_frames():
    global frame
    while running:
        success, img = cap.read()
        if success:
            frame = cv2.flip(img, 1)

# El algılama thread'i
def detect_hand():
    global current_hand, frame
    while running:
        if frame is not None:
            hands, _ = detector.findHands(frame, flipType=False, draw=False)
            if hands:
                current_hand = hands[0]['lmList'][8][:2]
            else:
                current_hand = None

# Quiz mantığı thread'i
def process_quiz():
    global qno, score, running, current_hand, frame
    debounce_time = 1  # Şık seçimi için bekleme süresi (saniye)
    last_interaction = time.time()

    while running:
        if frame is not None:
            img = frame.copy()

            if qno < qtotal:  # Sorular devam ediyorsa
                msq = quiz_list[qno]

                # Soruyu ve şıkları ekrana yazdır
                img, _ = cvzone.putTextRect(img, f"Question {qno + 1}/{qtotal}: {msq.question}", [50, 50], 2, 2, offset=50, border=2, colorR=(50, 50, 150), colorB=(0, 0, 0), colorT=(255, 255, 255))
                img, bbox1 = cvzone.putTextRect(img, msq.choice1, [50, 200], 2, 2, offset=20, border=2, colorB=msq.color_boxes[0], colorR=(50, 50, 150))
                img, bbox2 = cvzone.putTextRect(img, msq.choice2, [50, 300], 2, 2, offset=20, border=2, colorB=msq.color_boxes[1], colorR=(50, 50, 150))
                img, bbox3 = cvzone.putTextRect(img, msq.choice3, [50, 400], 2, 2, offset=20, border=2, colorB=msq.color_boxes[2], colorR=(50, 50, 150))
                img, bbox4 = cvzone.putTextRect(img, msq.choice4, [50, 500], 2, 2, offset=20, border=2, colorB=msq.color_boxes[3], colorR=(50, 50, 150))

                # Skoru yazdır
                img, _ = cvzone.putTextRect(img, f"Score: {score}", [900, 100], 2, 2, offset=10, border=2, colorB=(0, 0, 0), colorR=(50, 50, 150))

                # El algılama ve şık seçimi
                if current_hand and time.time() - last_interaction > debounce_time:
                    if not msq.answered:  # Soru daha önce cevaplanmamışsa
                        if msq.update(current_hand, [bbox1, bbox2, bbox3, bbox4]):
                            last_interaction = time.time()
                            if msq.useransw == msq.get_answer_index():
                                score += 1
                            qno += 1  # Sonraki soruya geç

            else:  # Tüm sorular bittiğinde
                img, _ = cvzone.putTextRect(img, "Game Over", [400, 300], 3, 3, offset=30, border=5, colorB=(0, 0, 255), colorR=(50, 50, 150))
                img, _ = cvzone.putTextRect(img, f"Your Score: {score}/{qtotal}", [400, 400], 2, 2, offset=20, border=3, colorB=(0, 0, 0), colorR=(50, 50, 150))

            cv2.imshow("Quiz Game", img)

        # Kullanıcıdan çıkış bekleme (ama ekran donmaz)
        if qno >= qtotal or cv2.waitKey(1) == ord('t'):  # Tüm sorular bittiyse
            if cv2.waitKey(1) == ord('t'):  # 't' tuşuna basılınca çıkış
                running = False
                break

        if cv2.waitKey(1) == ord('t'):
            running = False
            break


# Thread'leri başlat
capture_thread = threading.Thread(target=capture_frames)
detect_thread = threading.Thread(target=detect_hand)
quiz_thread = threading.Thread(target=process_quiz)

capture_thread.start()
detect_thread.start()
quiz_thread.start()

# Thread'leri bitir
capture_thread.join()
detect_thread.join()
quiz_thread.join()

cap.release()
cv2.destroyAllWindows()
