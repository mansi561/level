from typing import List
from fastapi import FastAPI, UploadFile, File
import face_recognition
import os
import psycopg2
app = FastAPI()
conn = psycopg2.connect(
    dbname="attendance",
    user="postgres",
    password="your_password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        encoding TEXT NOT NULL
    )
''')
@app.post("/register-face")
async def register_face(name: str, email: str, file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = face_recognition.load_image_file(img_bytes)
    encoding = face_recognition.face_encodings(img)[0]
    encoding_str = ','.join(map(str, encoding))
    cur.execute("INSERT INTO users (name, email, encoding) VALUES (%s, %s, %s)", (name, email, encoding_str))
    conn.commit()
    return {"message": "Face registered successfully"}
@app.post("/recognise-face")
async def recognise_face(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = face_recognition.load_image_file(img_bytes)
    encoding = face_recognition.face_encodings(img)[0]
    encoding_str = ','.join(map(str, encoding))
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    closest_match = None

    min_distance = float('inf')
    for row in rows:
        db_encoding = list(map(float, row[3].split(',')))
        distance = face_recognition.face_distance([db_encoding], encoding)[0]
        if distance < min_distance:
            closest_match = row
            min_distance = distance
    if closest_match:
        return {"name": closest_match[1], "email": closest_match[2]}
    else:
        return {"message": "No matching face found"}
@app.on_event("shutdown")
async def shutdown_event():
    cur.close()
    conn.close()

