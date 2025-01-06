import numpy as np
import cv2
from tensorflow.keras.models import load_model

turk_alphabet = [
    "a", "b", "c", "d", "e", "f", "g", "h", "ı", "i", "j", "k", "l", "m",
    "n", "o", "p", "r", "s", "t", "u", "v", "y", "z"
]

labels_path = "labels.txt"
with open(labels_path, 'r') as labelsfile:
    classes = [line.strip().split(' ', 1)[-1] for line in labelsfile.readlines()]
if len(classes) < len(turk_alphabet):
    classes = turk_alphabet

print("Classes:", classes)
model_path = "keras_model.h5"
model = load_model(model_path, compile=False)

output_size = model.output_shape[1]
if len(classes) != output_size:
    print(f"UYARI: Model {output_size} sınıf için eğitildi, ancak {len(classes)} sınıf verildi.")
    classes = classes[:output_size]  

cap = cv2.VideoCapture(0)
frameWidth = 1280
frameHeight = 720
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frameWidth)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frameHeight)
cap.set(cv2.CAP_PROP_GAIN, 0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Could not get camera image!")
        break

    frame = cv2.flip(frame, 1)  
    margin = int((frameWidth - frameHeight) / 2)
    square_frame = frame[0:frameHeight, margin:margin + frameHeight]

    resized_img = cv2.resize(square_frame, (224, 224))
    model_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    image_array = np.asarray(model_img)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    predictions = model.predict(data)
    confidence = np.max(predictions[0]) * 100
    predicted_index = np.argmax(predictions[0])
    predicted_label = classes[predicted_index]

    threshold = 50 
    if confidence > threshold:
        text = f"Guess: {predicted_label} (%{int(confidence)})"
    else:
        text = "Insufficient trust score"

    cv2.putText(
        img=square_frame,
        text=text,
        org=(50, 50),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=1,
        color=(255, 255, 255),
        thickness=2
    )

    cv2.imshow('Webcam View', square_frame)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break

cap.release()
cv2.destroyAllWindows()
