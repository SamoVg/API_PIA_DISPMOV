import face_recognition
import base64
import json
import numpy as np
from io import BytesIO
from PIL import Image

DB_FILE = "faces_db.json"

def load_db():
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f)

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

def save_face_encoding(name, image_bytes):
    encoding = image_to_encoding(image_bytes)
    if encoding is None:
        return "No face detected"

    db = load_db()
    db[name] = base64.b64encode(encoding.tobytes()).decode("utf-8")
    save_db(db)
    return "Saved"

def recognize_face(image_bytes):
    print("Reconociendo rostro...")
    
    # Cargar la base de datos (aquí se espera que db tenga nombres como claves y los valores sean las representaciones codificadas en base64)
    db = load_db()  
    
    # Generar el "encoding" de la imagen desconocida
    unknown_encoding = image_to_encoding(image_bytes)
    
    if unknown_encoding is None:
        return False
    
    # Iterar sobre todas las entradas de la base de datos para comparar las imágenes
    for name, encoded_face in db.items():
        known_encoding = np.frombuffer(base64.b64decode(encoded_face), dtype=np.float64)
        
        # Comparar la imagen desconocida con la imagen conocida
        match = face_recognition.compare_faces([known_encoding], unknown_encoding)[0]
        
        if match:
            return name  # Si hay coincidencia, devolver el nombre asociado a la imagen

    return False  # Si no se encuentra ninguna coincidencia