from typing import List
from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session

from app.schemas.movie import MovieOut, MovieIn, MovieUpdate
from app.services.service import is_cast_present
from app.db.pg_db import SessionLocal
from app.db.db_manager import add_movie, update_movie, get_all_movies, get_movie

movies = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@movies.post('/', response_model=MovieOut, status_code=201)
def create_movie(payload: MovieIn, db: Session = Depends(get_db)):
    for cast_id in payload.casts_id:
        if not is_cast_present(cast_id):
            raise HTTPException(status_code=404, detail=f"Cast with id:{cast_id} not found")

    movie_id = add_movie(db, payload)
    response = {
        'id': movie_id,
        **payload.dict()
    }

    return response

@movies.get('/', response_model=List[MovieOut])
def get_movies(db: Session = Depends(get_db)):
    movies = get_all_movies(db)
    return movies

@movies.get('/{id}/', response_model=MovieOut)
def get_movie(id: int, db: Session = Depends(get_db)):
    movie = get_movie(db, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@movies.put('/{id}/', response_model=MovieOut)
def update_movie(id: int, payload: MovieUpdate, db: Session = Depends(get_db)):
    movie = get_movie(db, id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    update_data = payload.dict(exclude_unset=True)

    if 'casts_id' in update_data:
        for cast_id in payload.casts_id:
            if not is_cast_present(cast_id):
                raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    movie_in_db = MovieIn(**movie)

    updated_movie = movie_in_db.copy(update=update_data)

    return update_movie(db, id, updated_movie)