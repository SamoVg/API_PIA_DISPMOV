from fastapi import APIRouter,UploadFile, File
from face_utils import  recognize_face,save_face_encoding

from utility.caras_json_factory import ObtenerCarasGrupo,AgregarCaraAlumno
from utility.grupo_json_factory import ObtenerAlumnoPorId,ObtenerIdAlumno
router = APIRouter(
    prefix="/FaceRecognition",
    tags=["Reconocimiento facial"]
)

@router.post("/ReconocerCara/{idGrupo}")
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

@router.post("/RegistrarCara/{grupo}")
async def register(matricula:int,grupo:str, image: UploadFile = File(...)):
    image_bytes = await image.read()
    imageEncode = save_face_encoding( image_bytes)
    idAlumno=ObtenerIdAlumno(matricula,grupo)
    if "error" in idAlumno:
        return {"error": idAlumno["error"]}
    faces= ObtenerCarasGrupo(grupo)
    if "error" in faces:
        return {"error": faces["error"]}
    match = recognize_face(image_bytes, faces)
    if match is not False:
        return {"error": "Ya existe una alumno registrado con esta cara."}
    result = AgregarCaraAlumno(idAlumno, grupo, imageEncode)
    if "error" in result:
        return {"error": result["error"]}
    return {"status": result}
