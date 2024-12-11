import cv2
import os
from pygame import mixer
import time
import threading
from gtts import gTTS

def generate_audio_files(class_names):
    for class_name in class_names:
        text = f"A {class_name} was detected."
        file_name = f"sounds/{class_name}.mp3"
        if not os.path.exists("sounds"):
            os.mkdir("sounds")
        if not os.path.exists(file_name):
            tts = gTTS(text, lang="en")
            tts.save(file_name)

def play_audio(class_name):
    def _play():
        file_name = f"sounds/{class_name}.mp3"
        if os.path.exists(file_name):
            mixer.init()
            mixer.music.load(file_name)
            mixer.music.play()
            while mixer.music.get_busy():
                time.sleep(0.1)

    threading.Thread(target=_play, daemon=True).start()

def initialize_model():
    net = cv2.dnn.readNet("dnn_model/yolov4-tiny.weights", "dnn_model/yolov4-tiny.cfg")
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(320, 320), scale=1 / 255)
    return model

# Load class list
def load_classes(file_path):
    classes = []
    with open(file_path, "r") as f:
        for line in f.readlines():
            classes.append(line.strip())
    return classes

# Main function
def main():
    # Define the classes and load model
    classes = load_classes("dnn_model/classes.txt")
    generate_audio_files(classes)
    model = initialize_model()

    detected_once = {class_name: False for class_name in classes}

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        (class_ids, scores, bboxes) = model.detect(frame, confThreshold=0.3, nmsThreshold=0.4)
        for class_id, score, bbox in zip(class_ids, scores, bboxes):
            (x, y, w, h) = bbox
            cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 0, 50), 3)

            class_name = classes[class_id]
            cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_PLAIN, 3, (200, 0, 50), 2)

            # Play sound only if not played before
            if not detected_once[class_name]:
                detected_once[class_name] = True
                play_audio(class_name)

        cv2.imshow("Object Detection", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the program
if __name__ == "__main__":
    main()
