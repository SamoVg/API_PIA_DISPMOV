from fastapi import APIRouter, UploadFile, File, Query
from face_utils import recognize_face
from utility.caras_json_factory import ObtenerCarasGrupo
from utility.grupo_json_factory import ObtenerAlumnoPorId, ObtenerAlumnosGrupoPorMatricula
from utility.asistencias_json_factory import RegistrarAsistenciaAlumno, ObtenerAsistencias
from datetime import datetime
from models.responseApi import ResponseWrapper  # Asegúrate que esta ruta sea correcta

router = APIRouter(
    prefix="/Asistencia",
    tags=["Asistencias"],
)

@router.post("/RegistrarAsistenciaHoy/{idGrupo}")
async def RegistrarAsistenciaHoy(idGrupo: str, image: UploadFile = File(...)):
    image_bytes = await image.read()
    faces = ObtenerCarasGrupo(idGrupo)
    if "error" in faces:
        return ResponseWrapper(success=False, message=faces["error"]).to_dict()

    match = recognize_face(image_bytes, faces)
    if match is False:
        return ResponseWrapper(success=False, message="No se encontró una coincidencia.").to_dict()
    if match is None:
        return ResponseWrapper(success=False, message="No se detectó ninguna cara en la imagen.").to_dict()

    alumno = ObtenerAlumnoPorId(match, idGrupo)
    if "error" in alumno:
        return ResponseWrapper(success=False, message=alumno["error"]).to_dict()

    resultAsistencia = RegistrarAsistenciaAlumno(idGrupo, str(datetime.now().date()), alumno["matricula"])
    if "error" in resultAsistencia:
        return ResponseWrapper(success=False, message=resultAsistencia["error"]).to_dict()

    return ResponseWrapper(data=alumno, message="Asistencia registrada correctamente").to_dict()

@router.post("/RegistrarAsistencia/{idGrupo}")
async def RegistrarAsistencia(idGrupo: str, image: UploadFile = File(...), fecha: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$")):
    image_bytes = await image.read()
    faces = ObtenerCarasGrupo(idGrupo)
    if "error" in faces:
        return ResponseWrapper(success=False, message=faces["error"]).to_dict()

    match = recognize_face(image_bytes, faces)
    if match is False:
        return ResponseWrapper(success=False, message="No se encontró una coincidencia.").to_dict()
    if match is None:
        return ResponseWrapper(success=False, message="No se detectó ninguna cara en la imagen.").to_dict()

    alumno = ObtenerAlumnoPorId(match, idGrupo)
    if "error" in alumno:
        return ResponseWrapper(success=False, message=alumno["error"]).to_dict()

    resultAsistencia = RegistrarAsistenciaAlumno(idGrupo, fecha, alumno["matricula"])
    if "error" in resultAsistencia:
        return ResponseWrapper(success=False, message=resultAsistencia["error"]).to_dict()

    return ResponseWrapper(data=alumno, message="Asistencia registrada correctamente").to_dict()

@router.get("/ObtenerAsistencias/{idGrupo}")
async def AsistenciasGrupo(idGrupo: str, fecha: str = Query(..., regex=r"^\d{4}-\d{2}-\d{2}$")):
    asistencias = ObtenerAsistencias(idGrupo, fecha)
    if "error" in asistencias:
        return ResponseWrapper(success=False, message=asistencias["error"]).to_dict()

    alumnos = ObtenerAlumnosGrupoPorMatricula(idGrupo, asistencias)
    if "error" in alumnos:
        return ResponseWrapper(success=False, message=alumnos["error"]).to_dict()

    return ResponseWrapper(data=alumnos, message="Asistencias obtenidas correctamente").to_dict()
