from fastapi import APIRouter,UploadFile, File,Query
from face_utils import  recognize_face
from utility.caras_json_factory import ObtenerCarasGrupo
from utility.grupo_json_factory import ObtenerAlumnoPorId,ObtenerAlumnosGrupo
from utility.asistencias_json_factory import RegistrarAsistenciaAlumno,ObtenerAsistencias
from datetime import datetime,timedelta

router = APIRouter(
    prefix="/Asistencia",
    tags=["Asistencias"],
)

@router.post("/RegistrarAsistenciaHoy/{idGrupo}")
async def RegistrarAsistenciaHoy(idGrupo:str, image: UploadFile = File(...)):
    fecha_hoy = datetime.now().date()
    fecha_manana = fecha_hoy + timedelta(days=1)
    fecha_str = str(fecha_manana)

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
    resultAsistencia = RegistrarAsistenciaAlumno(idGrupo, fecha_str, alumno["matricula"])
    if "error" in resultAsistencia:
        return {"error": resultAsistencia["error"]}
    if "error" in alumno:
        return {"error": alumno["error"]}
    
    return alumno

@router.get("/ObtenerAsistencias/{idGrupo}")
async def AsistenciasGrupo(idGrupo:str,fecha:str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$")):
    asistencias=ObtenerAsistencias(idGrupo,fecha)
    if "error" in asistencias:
        return {"error": asistencias["error"]}
    alumnos = ObtenerAlumnosGrupo(idGrupo,asistencias)
    if "error" in alumnos:
        return {"error": alumnos["error"]}
    
    return alumnos