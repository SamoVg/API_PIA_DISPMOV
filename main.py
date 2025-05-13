from fastapi import FastAPI, UploadFile, File, Form
from face_utils import save_face_encoding, recognize_face
from fastapi.middleware.cors import CORSMiddleware
import base64



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],      # Permite todos los métodos HTTP
    allow_headers=["*"]       # Permite todas las cabeceras
)

@app.get("/")
def read_root():
    return {"msg": "Hola mundo"}

@app.post("/register")
async def register(name: str = Form(...), image: UploadFile = File(...)):
    image_bytes = await image.read()
    result = save_face_encoding(name, image_bytes)
    return {"status": result}

@app.get("/recognize")
async def recognize(image: UploadFile = Form(...)):
    image_bytes = await image.read()
    match = recognize_face(image_bytes)
    return {"match": match}