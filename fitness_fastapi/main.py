from fastapi import FastAPI
from fitness_fastapi.routers import api_router

app = FastAPI(
    title="Fitness FastAPI",
    version="1.0.0"
)

app.include_router(api_router)
