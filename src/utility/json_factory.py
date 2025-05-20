import glob
import os
import json
import uuid
from  models.alumno import AlumnoModel

DB_RUTA = "./data/grupos"
DB_CARAS = "./data/caras/grupos_caras.json"

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
    AgregarGrupoACaras(identificadorGrupo)
    return {"status": "Grupo creado exitosamente con el nombre: "  + identificadorGrupo}


def AgregarGrupoACaras(identificadorGrupo: str):
    # Asegurar que la carpeta existe
    carpeta = os.path.dirname(DB_CARAS)
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Cargar datos existentes o crear nuevos
    if os.path.exists(DB_CARAS):
        with open(DB_CARAS, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = {}

    # Verificar si el grupo ya existe
    if identificadorGrupo in datos:
        return {"error": f"El grupo '{identificadorGrupo}' ya existe."}

    # Agregar el grupo
    datos[identificadorGrupo] = {
        "idGrupo": identificadorGrupo,
        "alumnosCaras": []
    }

    # Guardar el archivo actualizado
    with open(DB_CARAS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    return {"status": f"Grupo '{identificadorGrupo}' creado exitosamente"}

def AgregarCaraAlumno(idAlumno:str,idGrupo:str, cara:str):
    # Cargar datos existentes
    with open(DB_CARAS, "r", encoding="utf-8") as f:
        datos = json.load(f)

    # Verificar si el grupo existe
    if idGrupo not in datos:
        return {"error": f"El grupo '{idGrupo}' no existe."}

    # Agregar cara al alumno
    grupo = datos[idGrupo]
    if "alumnosCaras" not in grupo:
        grupo["alumnosCaras"] = []

    grupo["alumnosCaras"].append({
        "idAlumno": str(idAlumno),
        "cara": cara
    })

    # Guardar archivo actualizado
    with open(DB_CARAS, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    return {"status": "Cara agregada exitosamente", "idAlumno": str(idAlumno), "idGrupo": idGrupo}

def AgregarAlumnoGrupo(identificadorGrupo:str, alumno:AlumnoModel):
    ruta = os.path.join(DB_RUTA, f"{identificadorGrupo}.json")
    if not os.path.exists(ruta):
        return {"error": "El grupo no existe."}
    
    # Cargar datos existentes
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    # Agregar alumno al arreglo "alumnos"
    if "alumnos" not in datos:
        datos["alumnos"] = []

    datos["alumnos"].append(alumno.to_dict())

    # Guardar archivo actualizado
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    return {"status": "Alumno agregado exitosamente", "alumno": alumno.to_dict()}

def ObtenerIdAlumno(matricula:int, grupo:str):
    ruta = os.path.join(DB_RUTA, f"{grupo}.json")
    if not os.path.exists(ruta):
        return {"error": "El grupo no existe."}
    
    # Cargar datos existentes
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    # Buscar alumno por matrícula
    for alumno in datos["alumnos"]:
        if alumno["matricula"] == matricula:
            return alumno["idAlumno"]

    return {"error": "Alumno no encontrado."}