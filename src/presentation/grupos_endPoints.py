from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from utility.caras_json_factory import AgregarGrupoACaras
from utility.grupo_json_factory import CrearGrupo, AgregarAlumnoGrupo, ObtenerGrupos, ObtenerAlumnosGrupo
from utility.asistencias_json_factory import CrearGrupoAsistencias
from models.alumno import AlumnoRequest, AlumnoModel
from models.responseApi import ResponseWrapper  
import uuid

class FechaRequest(BaseModel):
    fecha: date

router = APIRouter(
    prefix="/Grupos",
    tags=["Grupos"]
)

@router.post("/CrearGrupo")
def create_group(identificadorGrupo: str):
    identificadorGrupo = identificadorGrupo.upper()
    response = CrearGrupo(identificadorGrupo)
    if "error" in response:
        return ResponseWrapper(success=False, message=response["error"]).to_dict()

    responseCaras = AgregarGrupoACaras(identificadorGrupo)
    if "error" in responseCaras:
        return ResponseWrapper(success=False, message=responseCaras["error"]).to_dict()

    responseAsistencias = CrearGrupoAsistencias(identificadorGrupo)
    if "error" in responseAsistencias:
        return ResponseWrapper(success=False, message=responseAsistencias["error"]).to_dict()

    return ResponseWrapper(data=response, message="Grupo creado correctamente").to_dict()

@router.post("/registrarAlumnoDatos/{grupo}")
async def register_student_data(Alumno: AlumnoRequest, grupo: str):
    alumno = AlumnoModel(
        idAlumno=uuid.uuid4(),
        nombres=Alumno.nombres,
        matricula=Alumno.matricula,
        apellidos=Alumno.apellidos
    )
    result = AgregarAlumnoGrupo(grupo, alumno)
    if "error" in result:
        return ResponseWrapper(success=False, message=result["error"]).to_dict()
    return ResponseWrapper(data=result, message="Alumno registrado correctamente").to_dict()

@router.get("/ObtenerTodosGrupos")
def get_all_groups():
    grupos = ObtenerGrupos()
    if "error" in grupos:
        return ResponseWrapper(success=False, message=grupos["error"]).to_dict()
    return ResponseWrapper(data=grupos, message="Grupos obtenidos exitosamente").to_dict()

@router.get("/ObtenerAlumnosGrupo/{grupo}")
def get_students_by_group(grupo: str):
    alumnos = ObtenerAlumnosGrupo(grupo)
    if "error" in alumnos:
        return ResponseWrapper(success=False, message=alumnos["error"]).to_dict()
    return ResponseWrapper(data=alumnos, message="Alumnos obtenidos exitosamente").to_dict()
