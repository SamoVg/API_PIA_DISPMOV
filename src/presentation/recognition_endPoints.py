from fastapi import APIRouter, UploadFile, File
from face_utils import recognize_face, save_face_encoding
from utility.caras_json_factory import ObtenerCarasGrupo, AgregarCaraAlumno
from utility.grupo_json_factory import ObtenerAlumnoPorId, ObtenerIdAlumno
from models.responseApi import ResponseWrapper  

router = APIRouter(
    prefix="/FaceRecognition",
    tags=["Reconocimiento facial"]
)

@router.post("/ReconocerCara/{idGrupo}")
async def recognize(idGrupo: str, image: UploadFile = File(...)):
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

    return ResponseWrapper(data=alumno, message="Alumno reconocido correctamente").to_dict()
@router.post("/RegistrarCara/{grupo}")
async def register(matricula: int, grupo: str, image: UploadFile = File(...)):
    image_bytes = await image.read()
    imageEncode = save_face_encoding(image_bytes)

    idAlumno = ObtenerIdAlumno(matricula, grupo)
    if "error" in idAlumno:
        return ResponseWrapper(success=False, message=idAlumno["error"]).to_dict()

    faces = ObtenerCarasGrupo(grupo)
    if "error" in faces:
        return ResponseWrapper(success=False, message=faces["error"]).to_dict()

    match = recognize_face(image_bytes, faces)
    if match is not False:
        return ResponseWrapper(success=False, message="Ya existe un alumno registrado con esta cara.").to_dict()

    result = AgregarCaraAlumno(idAlumno, grupo, imageEncode)
    if "error" in result:
        return ResponseWrapper(success=False, message=result["error"]).to_dict()

    return ResponseWrapper(data=result, message="Cara registrada correctamente").to_dict()
