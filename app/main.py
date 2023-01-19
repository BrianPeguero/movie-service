from fastapi import FastAPI
from app.apis.movie import movies

app = FastAPI(openapi_url="/api/v1/movie-service/openapi.json", docs_url="/api/v1/movie-service/docs")

app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])