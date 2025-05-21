from fastapi import APIRouter
from pydantic import BaseModel
from pydantic import BaseModel
from datetime import  date
from utility.caras_json_factory import AgregarGrupoACaras
from utility.grupo_json_factory import CrearGrupo, AgregarAlumnoGrupo,ObtenerGrupos,ObtenerAlumnosGrupo
from utility.asistencias_json_factory import CrearGrupoAsistencias
from  models.alumno import AlumnoRequest,AlumnoModel
import uuid
class FechaRequest(BaseModel):
    fecha: date
    
router=APIRouter(
    prefix="/Grupos",
    tags=["Grupos"]
)

@router.post("/CrearGrupo")
def create_group(identificadorGrupo:str ):
    identificadorGrupo.upper()
    response =CrearGrupo(identificadorGrupo)
    if("error" in response):
        return {"error": response["error"]}
    responseCaras = AgregarGrupoACaras(identificadorGrupo)
    if("error" in responseCaras):
        return {"error": responseCaras["error"]}
    responseAsistencias = CrearGrupoAsistencias(identificadorGrupo)
    if("error" in responseAsistencias):
        return {"error": responseAsistencias["error"]}
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

@router.get("/ObtenerTodosGrupos")
def get_all_groups():
    grupos=ObtenerGrupos()
    if("error" in grupos):
        return {"error": grupos["error"]}
    return grupos

@router.get("/ObtenerAlumnosGrupo/{grupo}")
def get_students_by_group(grupo:str):
    alumnos=ObtenerAlumnosGrupo(grupo)
    if("error" in alumnos):
         return {"error": alumnos["error"]}
    return alumnos