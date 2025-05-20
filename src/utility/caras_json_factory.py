import os
import json
from  models.alumno import AlumnoModel

DB_CARAS = "./data/caras/grupos_caras.json"

def AgregarGrupoACaras(identificadorGrupo: str):
    carpeta = os.path.dirname(DB_CARAS)
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    if os.path.exists(DB_CARAS):
        with open(DB_CARAS, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = {}

    if identificadorGrupo in datos:
        return {"error": f"El grupo '{identificadorGrupo}' ya existe."}

    datos[identificadorGrupo] = {
        "idGrupo": identificadorGrupo,
        "alumnosCaras": []
    }

    with open(DB_CARAS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    return {"status": f"Grupo '{identificadorGrupo}' creado exitosamente"}

def AgregarCaraAlumno(idAlumno:str,idGrupo:str, cara:str):
    with open(DB_CARAS, "r", encoding="utf-8") as f:
        datos = json.load(f)

    if idGrupo not in datos:
        return {"error": f"El grupo '{idGrupo}' no existe."}

    grupo = datos[idGrupo]
    if "alumnosCaras" not in grupo:
        grupo["alumnosCaras"] = []

    grupo["alumnosCaras"].append({
        "idAlumno": str(idAlumno),
        "cara": cara
    })

    with open(DB_CARAS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    return {"status": "Cara agregada exitosamente", "idAlumno": str(idAlumno), "idGrupo": idGrupo}

def ObtenerCarasGrupo(idGrupo:str):
    with open(DB_CARAS,"r",encoding="utf-8") as f:
        datos = json.load(f)
    if idGrupo not in datos:
        return {"error": f"El grupo '{idGrupo}' no existe."}
    grupo = datos[idGrupo]
    if "alumnosCaras" not in grupo:
        return {"error": f"El grupo '{idGrupo}' no tiene caras registradas."}
    return grupo["alumnosCaras"]
