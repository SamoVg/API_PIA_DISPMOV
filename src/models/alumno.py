from dataclasses import dataclass
from pydantic import BaseModel
from typing import List
import uuid
from typing import Optional

class AlumnoRequest(BaseModel):
    nombres: str
    matricula: int
    apellidos:str
    
    

@dataclass
class AlumnoModel:
    idAlumno: uuid.UUID
    nombres: str
    matricula: int
    apellidos: str
    idCara:int=0
    def to_dict(self):
        return {
            "idAlumno": str(self.idAlumno),
            "nombres": self.nombres,
            "matricula": self.matricula,
            "apellidos": self.apellidos,
            "idCara": self.idCara
        }
