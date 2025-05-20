import face_recognition
import base64
import numpy as np
from io import BytesIO
from PIL import Image

def image_to_encoding(image_bytes):
    image = Image.open(BytesIO(image_bytes)).convert("RGB")

    # OPCIÓN 1: Redimensionar imagen si es muy grande (por encima de 1600px)
    MAX_SIZE = 1024
    if image.width > MAX_SIZE or image.height > MAX_SIZE:
        image.thumbnail((MAX_SIZE, MAX_SIZE))  # Mantiene proporciones

    np_image = np.array(image)
    print("detectando")
    # OPCIÓN 2: Usar modelo 'cnn' (más preciso, pero más lento)
    face_locations = face_recognition.face_locations(np_image)

    if not face_locations:
        return None

    encodings = face_recognition.face_encodings(np_image, face_locations)
    return encodings[0] if encodings else None

def save_face_encoding(image_bytes):
    encoding = image_to_encoding(image_bytes)
    if encoding is None:
        return "No face detected"
    encode = base64.b64encode(encoding.tobytes()).decode("utf-8")
    return encode

def recognize_face(image_bytes, items):
    print("Reconociendo rostro...")

    # Generar el encoding de la imagen desconocida
    unknown_encoding = image_to_encoding(image_bytes)

    if unknown_encoding is None:
        return False

    # Iterar sobre la lista de diccionarios con 'idAlumno' y 'cara'
    for alumno in items:
        id_alumno = alumno.get("idAlumno")
        cara_base64 = alumno.get("cara")

        if not id_alumno or not cara_base64:
            continue  # Ignorar si falta algún dato

        try:
            known_encoding = np.frombuffer(base64.b64decode(cara_base64), dtype=np.float64)
        except Exception as e:
            print(f"Error al decodificar la cara de {id_alumno}: {e}")
            continue

        match = face_recognition.compare_faces([known_encoding], unknown_encoding)[0]

        if match:
            return id_alumno

    return False