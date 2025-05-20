from fastapi import APIRouter,UploadFile, File
from face_utils import  recognize_face
from utility.caras_json_factory import ObtenerCarasGrupo
from utility.grupo_json_factory import ObtenerAlumnoPorId
router = APIRouter(
    prefix="/Asistencia",
    tags=["Asistencias"]
)

@router.post("/RegistrarAsistencia/{idGrupo}")
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

