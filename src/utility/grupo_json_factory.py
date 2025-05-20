import os
import json
from  models.alumno import AlumnoModel
DB_RUTA = "./data/grupos"

def CrearGrupo(identificadorGrupo:str ):
    print("Creando grupo con el nombre: " + identificadorGrupo)

    ruta = os.path.join(DB_RUTA, f"{identificadorGrupo}.json")
    if os.path.exists(ruta):
        return {"error": "El grupo ya existe."}
    datos ={
        "idGrupo": identificadorGrupo,
        "alumnos":[]
    }
    print("Creando grupo con el nombre: " + identificadorGrupo)
    with open(ruta, "w", encoding="utf-8") as f:
       json.dump(datos, f, ensure_ascii=False, indent=4)
    return {"status": "Grupo creado exitosamente con el nombre: "  + identificadorGrupo}

def AgregarAlumnoGrupo(identificadorGrupo:str, alumno:AlumnoModel):
    ruta = os.path.join(DB_RUTA, f"{identificadorGrupo}.json")
    if not os.path.exists(ruta):
        return {"error": "El grupo no existe."}
    
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    if "alumnos" not in datos:
        datos["alumnos"] = []
    if any(a["matricula"] == alumno.matricula for a in datos["alumnos"]):
        return {"error": "esta matricula ya está registrado en el grupo."}
    datos["alumnos"].append(alumno.to_dict())

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    return {"status": "Alumno agregado exitosamente", "alumno": alumno.to_dict()}

def ObtenerIdAlumno(matricula:int, grupo:str):
    ruta = os.path.join(DB_RUTA, f"{grupo}.json")
    if not os.path.exists(ruta):
        return {"error": "El grupo no existe."}
    
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    for alumno in datos["alumnos"]:
        if alumno["matricula"] == matricula:
            return alumno["idAlumno"]

    return {"error": "Alumno no encontrado."}
def ObtenerAlumnoPorId(idAlumno:str,grupo:str):
    ruta = os.path.join(DB_RUTA, f"{grupo}.json")
    if not os.path.exists(ruta):
        return {"error": "El grupo no existe."}
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
    for alumno in datos["alumnos"]:
        if alumno["idAlumno"] == idAlumno:
            return alumno
    
def ObtenerAlumnosGrupo(grupo:str,matriculas:list):
    ruta = os.path.join(DB_RUTA, f"{grupo}.json")
    if not os.path.exists(ruta):
        return {"error": "El grupo no existe."}
    
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
    alumnos = [alumno for alumno in datos["alumnos"] if alumno["matricula"] in matriculas]
    return alumnos