from fastapi import FastAPI, UploadFile, File, Form
from face_utils import save_face_encoding, recognize_face
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime, date
from utility.caras_json_factory import AgregarCaraAlumno,AgregarGrupoACaras,ObtenerCarasGrupo
from utility.grupo_json_factory import CrearGrupo, AgregarAlumnoGrupo, ObtenerIdAlumno,ObtenerAlumnoPorId
from  models.alumno import AlumnoRequest,AlumnoModel
import uuid
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],      
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
    if("error" in response):
        return {"error": response["error"]}
    responseCaras = AgregarGrupoACaras(identificadorGrupo)
    if("error" in responseCaras):
        return {"error": responseCaras["error"]}
    return response
  
@app.post("/RegistrarCara/{grupo}")
async def register(matricula:int,grupo:str, image: UploadFile = File(...)):
    image_bytes = await image.read()
    imageEncode = save_face_encoding( image_bytes)
    idAlumno=ObtenerIdAlumno(matricula,grupo)
    if "error" in idAlumno:
        return {"error": idAlumno["error"]}
    result = AgregarCaraAlumno(idAlumno, grupo, imageEncode)
    if "error" in result:
        return {"error": result["error"]}
    return {"status": result}

@app.post("/registrarAlumnoDatos/{grupo}")
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

@app.post("/ReconocerCara/{idGrupo}")
async def recognize(idGrupo:str, image: UploadFile = File(...)):
    image_bytes = await image.read()
    faces= ObtenerCarasGrupo(idGrupo)
    if "error" in faces:
        return {"error": faces["error"]}
    match = recognize_face(image_bytes, faces)
    if match is False:
        return {"error": "No se encontró una coincidencia."}
    if match is None:
        return {"error": "No se detectó ninguna cara en la imagen."}
    alumno = ObtenerAlumnoPorId(match,idGrupo)
    if "error" in alumno:
        return {"error": alumno["error"]}
    
    return alumno