from fastapi import FastAPI, UploadFile, File, Form
from face_utils import save_face_encoding, recognize_face
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic import BaseModel, validator
from datetime import datetime, date
from utility.json_factory import CrearGrupo,AgregarAlumnoGrupo,AgregarCaraAlumno,ObtenerIdAlumno
from  models.alumno import AlumnoRequest,AlumnoModel
import uuid
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],      # Permite todos los métodos HTTP
    allow_headers=["*"]         
)
class FechaRequest(BaseModel):
    fecha: date

@app.post("/ObtenerListaDia")
async def get_lista(request: FechaRequest):
  return {
        "fecha_recibida": request.fecha,
        "tipo": str(type(request.fecha))
    }
@app.post("/CrearGrupo")
def create_group(identificadorGrupo:str ):
    identificadorGrupo.upper()
    response =CrearGrupo(identificadorGrupo)
    return response
  
@app.post("/registerFace")
async def register(matricula:int,idGrupo:str, image: UploadFile = File(...)):
    image_bytes = await image.read()
    imageEncode = save_face_encoding( image_bytes)
    idAlumno=ObtenerIdAlumno(matricula,idGrupo)
    if "error" in idAlumno:
        return {"error": idAlumno["error"]}
    result = AgregarCaraAlumno(idAlumno, idGrupo, imageEncode)
    if "error" in result:
        return {"error": result["error"]}
    return {"status": result}

@app.post("/registrarAlumnoDatos")
async def register_student_data(Alumno: AlumnoRequest,grupo:str):
    alumno = AlumnoModel(
        idAlumno=uuid.uuid4(),
        nombres=Alumno.nombres,
        matricula=Alumno.matricula,
        apellidos=Alumno.apellidos
    )
    print("alumno creado con :")
    print(alumno)
    result = AgregarAlumnoGrupo(grupo, alumno)
    return result

@app.post("/recognize")
async def recognize(image: UploadFile = File(...)):
    image_bytes = await image.read()
    match = recognize_face(image_bytes)
    return {"match": match}