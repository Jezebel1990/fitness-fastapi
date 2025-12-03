from fastapi import APIRouter
from fitness_fastapi.praticante.controller import router as praticante
from fitness_fastapi.categorias.controller import router as categorias

api_router = APIRouter()
api_router.include_router(praticante, prefix="/praticantes", tags=["praticantes"])
api_router.include_router(categorias, prefix="/categorias", tags=["categorias"])