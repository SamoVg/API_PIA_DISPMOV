from fastapi import APIRouter,UploadFile, File
from face_utils import save_face_encoding, recognize_face
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pydantic import BaseModel
from datetime import datetime, date
from utility.caras_json_factory import AgregarCaraAlumno,AgregarGrupoACaras,ObtenerCarasGrupo
from utility.grupo_json_factory import CrearGrupo, AgregarAlumnoGrupo, ObtenerIdAlumno,ObtenerAlumnoPorId
from  models.alumno import AlumnoRequest,AlumnoModel
import uuid
class FechaRequest(BaseModel):
    fecha: date
    
router=APIRouter(
    prefix="/Grupos",
    tags=["Grupos"]
)

@router.post("/ObtenerListaDia")
async def get_lista(request: FechaRequest):
  return {
        "fecha_recibida": request.fecha,
        "tipo": str(type(request.fecha))
    }
@router.post("/CrearGrupo")
def create_group(identificadorGrupo:str ):
    identificadorGrupo.upper()
    response =CrearGrupo(identificadorGrupo)
    if("error" in response):
        return {"error": response["error"]}
    responseCaras = AgregarGrupoACaras(identificadorGrupo)
    if("error" in responseCaras):
        return {"error": responseCaras["error"]}
    return response
  

@router.post("/registrarAlumnoDatos/{grupo}")
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