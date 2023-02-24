import cv2
import tkinter as tk
from tkinter import filedialog
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
def register_face():
    file_path = filedialog.askopenfilename()
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) != 1:
        error_label.config(text="Error: please select an image with exactly one face")
    else:
        (x, y, w, h) = faces[0]
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100))
        (label, confidence) = face_recognizer.predict(face)
        if confidence < 50:
            result_label.config(text=f"Recognized face ID: {label}")
        else:
            result_label.config(text="No matching face found")
root = tk.Tk()
root.title("Face Recognition")
register_button = tk.Button(root, text="Register Face", command=register_face)
register_button.pack(pady=10)
recognize_button = tk.Button(root, text="Recognize Face", command=recognize_face)
recognize_button.pack(pady=10)
error_label = tk.Label(root, fg="red")
error_label.pack(pady=10)
result_label = tk.Label(root)