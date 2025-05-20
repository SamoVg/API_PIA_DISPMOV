import os
import json
from  models.alumno import AlumnoModel
DB_RUTA = "./data/asistencias"

def CrearGrupoAsistencias(identificadorGrupo:str ):
    print("Creando grupo con el nombre: " + identificadorGrupo)

    ruta = os.path.join(DB_RUTA, f"{identificadorGrupo}.json")
    if os.path.exists(ruta):
        return {"error": "El grupo ya existe."}
    datos ={
        "Asistencias":{}
    }
    print("Creando grupo con el nombre: " + identificadorGrupo)
    with open(ruta, "w", encoding="utf-8") as f:
       json.dump(datos, f, ensure_ascii=False, indent=4)
    return {"status": "Grupo creado exitosamente con el nombre: "  + identificadorGrupo}

def RegistrarAsistenciaAlumno(Grupo:str,Fecha:str,Matricula:str):
    ruta = os.path.join(DB_RUTA, f"{Grupo}.json")
    if not os.path.exists(ruta):
        return {"error": "El grupo no existe."}
    
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    if Fecha not in datos["Asistencias"]:
        datos["Asistencias"][Fecha] = []

    datos["Asistencias"][Fecha].append(Matricula)

    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)

    return {"status": "Asistencia registrada exitosamente", "Grupo": Grupo, "Fecha": Fecha, "Matricula": Matricula}

def ObtenerAsistencias(Grupo:str,Fecha:str):
    
    ruta = os.path.join(DB_RUTA, f"{Grupo}.json")
    if not os.path.exists(ruta):
        return {"error": "El grupo no existe."}
    
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)

    if Fecha not in datos["Asistencias"]:
        return {"error": "No hay asistencias registradas para esta fecha."}

    return datos["Asistencias"][Fecha]