import cv2
import numpy as np
from ultralytics import YOLO
import pyttsx3

# Text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load YOLO model
model = YOLO("yolov8n.pt")  # Tiny model for speed

# Open webcam (0 = default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    speak("Camera not found")
    print("Camera not found")
    exit()

speak("System started. Scanning for obstacles.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    detected_objects = []

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0]

            # YOLO class names
            class_name = model.names[cls]

            # Only speak important objects
            if class_name in ["person", "car", "bus", "truck", "motorcycle", "bicycle"]:
                detected_objects.append(class_name)

            # Draw on screen
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"{class_name} {conf:.2f}",
                (int(x1), int(y1) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

    # Speak if something relevant appears
    if detected_objects:
        speak("Warning. " + ", ".join(detected_objects) + " ahead.")

    cv2.imshow("Scanner", frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
