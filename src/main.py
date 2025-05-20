from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation import recognition_endPoints,grupos_endPoints,asistencias_endPoints
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],      
    allow_headers=["*"]         
)
app.include_router(recognition_endPoints.router)
app.include_router(grupos_endPoints.router)
app.include_router(asistencias_endPoints.router)

